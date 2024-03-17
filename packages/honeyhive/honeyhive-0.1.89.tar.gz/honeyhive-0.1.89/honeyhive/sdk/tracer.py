import sys
import json
import time
import uuid
import traceback
import datetime
import inspect
from litellm.utils import ModelResponse

from openai import OpenAI

from .sessions import start, end, log_event


class HoneyHiveTraceContextManager:
    def __init__(self, tracer):
        self.tracer = tracer
        self.event_id = tracer.event_id
        self.original_trace_function = None
        self.first_call_value = None
        self.last_return_value = None
        self.recorded_exception = None
        self.event_data = {
            "event_name": self.tracer.event_name,
            "input": {},
            "output": "",
            "error": None,
            "metadata": {},
            "duration": 0,
        }
        self.start_time = None
        self.end_time = None
        self.output = None

    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.general_trace_call)
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        sys.settrace(self.original_trace_function)
        self.prepare_input()
        self.prepare_output()
        self.prepare_error(exc_type, exc_val)
        self.tracer.log_event_with_data(self.event_data)

    def prepare_input(self):
        # prepare input, output, metadata, duration, error
        if 'kwargs' in self.first_call_value:
            temp = dict(self.first_call_value['kwargs'])
            del self.first_call_value['kwargs']
            for key, value in temp.items():
                # if value is an object, convert to dict
                if hasattr(value, '__dict__'):
                    self.first_call_value[key] = value.__dict__
                else:
                    self.first_call_value[key] = value
        if 'args' in self.first_call_value:
            temp = self.first_call_value['args']
            # if args is a tuple, convert to list
            if isinstance(temp, tuple):
                temp = list(temp)
            self.first_call_value['args'] = temp

        # drop anything that's non-JSON serializable
        new_call_value = {}
        for key, value in self.first_call_value.items():
            try:
                json.dumps(value)
                new_call_value[key] = value
            except TypeError:
                pass
        if self.tracer.input != None and self.tracer.input != {}:
            # put it in metadata
            self.event_data['metadata']['input'] = new_call_value
        else:
            self.event_data['input'] = new_call_value
        ##print("left call for set context")

        # go through the input & metadata.input, check if there are any tuple fields within 2 levels of nesting
        # if there are, convert them to lists
        if self.event_data['input'] != None:
            for key, value in self.event_data['input'].items():
                if isinstance(value, tuple):
                    self.event_data['input'][key] = list(value)
                elif isinstance(value, dict):
                    for key2, value2 in value.items():
                        if isinstance(value2, tuple):
                            self.event_data['input'][key][key2] = list(value2)
            # drop "positional", "variants" from input
            if 'positional' in self.event_data['input']:
                del self.event_data['input']['positional']
            if 'variants' in self.event_data['input']:
                del self.event_data['input']['variants']
        
        if self.event_data['metadata'] != None and 'input' in self.event_data['metadata']:
            for key, value in self.event_data['metadata']['input'].items():
                if isinstance(value, tuple):
                    self.event_data['metadata']['input'][key] = list(value)
                elif isinstance(value, dict):
                    for key2, value2 in value.items():
                        if isinstance(value2, tuple):
                            self.event_data['metadata']['input'][key][key2] = list(value2)
    
    def prepare_output(self):
        #print("prepare output")
        if self.last_return_value == None:
            return
        if type(self.last_return_value) is ModelResponse:
            self.last_return_value = self.last_return_value.json()

        if type(self.last_return_value) is dict:
            pass
        else:
            try:
                if hasattr(self.last_return_value, '__dict__'):
                    self.last_return_value = dict(self.last_return_value)
                else:
                    self.last_return_value = dict(json.loads(self.last_return_value))
            except:
                pass
        
        #print(type(self.last_return_value))
        if isinstance(self.last_return_value, dict):
            for key, value in self.last_return_value.items():
                # check if output_field contains a "."
                contains_dot = self.tracer.output_field.find(".")

                if contains_dot == False and key == self.tracer.output_field:
                    self.event_data['output'] = value
                elif contains_dot != False and key == self.tracer.output_field.split(".")[0]:
                    # with each split of the output_field, check if the key exists and get the value
                    # if the key doesn't exist, set it on metadata
                    split_output_field = self.tracer.output_field.split(".")
                    temp = self.last_return_value

                    for i in range(len(split_output_field)):
                        #print(split_output_field[i])
                        type_converted = False
                        # check if split_output_field[i] can be parsed as an int
                        # if it can, convert it to an int
                        try:
                            split_output_field[i] = int(split_output_field[i])
                            type_converted = True
                        except:
                            pass

                        if type_converted == False and split_output_field[i] in temp:
                            temp = temp[split_output_field[i]]
                        elif type_converted == True and isinstance(temp, list) and split_output_field[i] < len(temp):
                            temp = temp[split_output_field[i]]
                        else:
                            if self.event_data['metadata'] == None:
                                self.event_data['metadata'] = {}
                            self.event_data['metadata'][split_output_field[i]] = temp
                            break
                    
                    self.event_data['output'] = temp
                else:
                    if self.event_data['metadata'] == None:
                        self.event_data['metadata'] = {}
                    # if value has __dict__ attribute, convert to dict
                    if hasattr(value, '__dict__'):
                        self.event_data['metadata'][key] = value.__dict__
                    else:
                        self.event_data['metadata'][key] = value
        else:
            try:
                self.event_data['output'] = self.last_return_value
            except:
                pass
            finally:
                if self.event_data['metadata'] == None:
                    self.event_data['metadata'] = {}
                if self.event_data['output'] == "":
                    self.event_data['metadata']['output'] = self.last_return_value
        
        self.event_data['duration'] = (self.end_time - self.start_time) * 1000

        self.output = str(self.event_data["output"])
        # removed the redundant  str -> dict as its handled in sessions.py
        # sessions.log_event( requests a string

    def prepare_error(self, ex_type, ex_value):
        if ex_type == None:
            return
        ex_type = str(ex_type)
        ##print(self.recorded_exception)
        self.event_data['error'] = ex_type
        if self.event_data['metadata'] == None:
            self.event_data['metadata'] = {}
        self.event_data['metadata']["error_message"] = str(ex_value)
        self.event_data['duration'] = (self.end_time - self.start_time) * 1000

    def general_trace_call(self, frame, event, arg):
        if event == 'call' and self.first_call_value == None:
            self.first_call_value = frame.f_locals
            if self.event_data['event_name'] == "":
                self.event_data['event_name'] = frame.f_code.co_name
        elif event == 'return':
            self.last_return_value = arg

        return self.general_trace_call


class HoneyHiveTracer:
    def __init__(
        self, project, name, source="", user_properties={}, show_trace=False
    ):
        # get the name of the file where this is being called
        # if source is not provided, use that as the source
        if source == "":
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            source = module.__file__
            # don't include the directory stuff
            source = source.split("/")[-1]
        honeyhive_session = start(
            project=project,
            source=source,
            session_name=name,
            user_properties=user_properties,
        )
        self.events = []
        self.project = project
        self.source = source
        self.session_id = honeyhive_session.session_id
        self.event_id = None
        self.parent_id = None
        self.event_type = "model"
        self.event_name = ""
        self.config = {"provider": "", "endpoint": ""}
        self.children = []
        self.input = {}
        self.output = {}
        self.error = None
        self.duration = 0
        self.user_properties = user_properties
        self.metadata = {}
        self.context_set = False
        self.context_set_properly = False
        self.context_function_name = ""
        self.context_file_name = ""
        self.start_time = 0
        self.end_time = 0
        self.call_value = None
        self.return_value = None
        self.show_trace = show_trace

    def trace_calls(self, frame, event, arg):
        function_name = frame.f_code.co_name
        file_name = frame.f_code.co_filename

        print(f"function_name: {function_name}")
        print(f"file_name: {file_name}")
        print(f"event: {event}")

        if event == 'call':
            if function_name == "create" and file_name == inspect.getfile(OpenAI.completions):
                self.start_event()
                self.config['provider'] = "openai"
                self.config['endpoint'] = "completion"
                self.event_type = "model"
                self.call_value = frame.f_locals['kwargs']
                for key, value in self.call_value.items():
                    if key != "prompt":
                        self.config[key] = value
                    elif self.input == None or self.input == {}:
                        self.input = value
            elif function_name == "create" and file_name == inspect.getfile(
                OpenAI.chat.completions
            ):
                self.start_event()

                self.config['provider'] = "openai"
                self.config['endpoint'] = "chat"
                self.event_type = "model"
                self.call_value = frame.f_locals['kwargs']
                for key, value in self.call_value.items():
                    if key != "messages":
                        self.config[key] = value
                    elif self.input == None or self.input == {}:
                        self.input = value
            elif self.context_set and (
                function_name == self.context_function_name
                and file_name == self.context_file_name
            ):
                self.start_event(self.event_type)
                self.context_set_properly = True
                ##print("inside call for set context")
                ##print(function_name)
                ##print(file_name)
                ##print(frame.f_locals)

                self.call_value = frame.f_locals
                if 'kwargs' in self.call_value:
                    temp = dict(self.call_value['kwargs'])
                    del self.call_value['kwargs']
                    for key, value in temp.items():
                        self.call_value[key] = value
                if 'args' in self.call_value:
                    temp = self.call_value['args']
                    # if args is a tuple, convert to list
                    if isinstance(temp, tuple):
                        temp = list(temp)
                    self.call_value['args'] = temp

                # drop anything that's non-JSON serializable
                new_call_value = {}
                for key, value in self.call_value.items():
                    try:
                        json.dumps(value)
                        new_call_value[key] = value
                    except TypeError:
                        pass
                if self.input:
                    # put it in metadata
                    self.metadata['input'] = new_call_value
                else:
                    self.input = new_call_value
                ##print("left call for set context")
        elif event == 'exception':
            if function_name == "create" and (
                file_name == inspect.getfile(OpenAI.chat.completions)
                or file_name == inspect.getfile(OpenAI.completion)
            ):
                # from the exception, get the message and type
                ##print("exception")
                ex_type, ex_value, ex_traceback = arg
                ex_type = str(ex_type).split(".")[2][:-2]
                self.error = ex_type
                self.metadata["error_message"] = str(ex_value)
                self.log_event()
            elif (
                self.context_set
                and self.context_set_properly
                and (
                    function_name == self.context_function_name
                    and file_name == self.context_file_name
                )
            ):
                ##print("inside exception for set context")
                ##print(function_name)
                ##print(file_name)
                ex_type, ex_value, ex_traceback = arg
                ex_type = str(ex_type)
                self.error = ex_type
                self.metadata["error_message"] = str(ex_value)
                # print out the traceback
                traceback.print_tb(ex_traceback)
                self.log_event()
                ##print("left exception for set context")
        elif event == 'return':
            if function_name == "create" and file_name == inspect.getfile(OpenAI.completions):
                self.end_time = time.time()
                self.return_value = arg
                self.duration = (self.end_time - self.start_time) * 1000
                if self.return_value:
                    for key, value in self.return_value.items():
                        if key == "model":
                            self.config[key] = value
                        elif key == "created_at":
                            # turn created_at from utc number to isoformat
                            self.metadata[key] = datetime.fromtimestamp(
                                value
                            ).isoformat()
                        elif key == "choices":
                            self.output = value[0].text
                        elif key == "usage":
                            for key, value in value.items():
                                self.metadata[key] = value
                if arg:
                    arg['event_id'] = self.event_id
                self.log_event()
            elif function_name == "create" and file_name == inspect.getfile(OpenAI.chat.completions):
                print("inside return for openai chat")
                self.end_time = time.time()
                self.return_value = arg
                self.duration = (self.end_time - self.start_time) * 1000
                if self.return_value:
                    if type(self.return_value) is not dict:
                        self.return_value = self.return_value.__dict__
                    for key, value in self.return_value.items():
                        if key == "model":
                            self.config[key] = value
                        elif key == "created_at":
                            # turn created_at from utc number to isoformat
                            self.config[key] = datetime.fromtimestamp(
                                value
                            ).isoformat()
                        elif key == "choices":
                            self.output = value[0].message
                        elif key == "usage":
                            for key, value in value.items():
                                self.metadata[key] = value
                self.log_event()
            elif (
                self.context_set
                and self.context_set_properly
                and (
                    function_name == self.context_function_name
                    and file_name == self.context_file_name
                )
            ):
                print("inside return for set context")
                ##print(function_name)
                ##print(file_name)
                self.return_value = arg
                self.end_time = time.time()
                self.duration = (self.end_time - self.start_time) * 1000
                # print(self.return_value)
                # print(type(self.return_value))
                # check if return_value is of type dict
                if self.return_value:
                    if isinstance(self.return_value, dict):
                        for key, value in self.return_value.items():
                            if key == self.output_field:
                                self.output = value
                            else:
                                self.metadata[key] = value
                    else:
                        self.output = self.return_value
                ##print("left return for set context")
                self.log_event()

        return self.trace_calls

    def start_event(self, event_type="model", parent_id=None):
        if self.event_id == None:
            self.event_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.event_type = event_type
        self.output = {}
        self.duration = 0
        self.call_value = None
        self.return_value = None
        self.error = None
        self.metadata = {}
        if parent_id:
            self.parent_id = parent_id
        else:
            self.parent_id = self.session_id

    def log_event(self):
        #print("Logging event")
        if self.show_trace:
            self.print_event()
        
        if self.event_name == "openai_chat":
            self.output = self.output.message.model_dump()
            # drop any fields whose value is None from self.output
            self.output = {k: v for k, v in self.output.items() if v is not None}
            self.input["chat_history"] = self.input["messages"]
        
        log_event(
            session_id=self.session_id,
            project=self.project,
            event_id=self.event_id,
            event_name=self.event_name,
            event_type=self.event_type,
            source=self.source,
            config=self.config,
            input=self.input,
            output=self.output,
            error=self.error,
            duration=self.duration,
            metadata=self.metadata,
            user_properties=self.user_properties,
            children=self.children,
            parent_id=self.parent_id if self.parent_id else self.session_id,
        )

        # reset the event
        self.event_id = None
        self.event_type = "model"
        self.event_name = ""
        self.config = {}
        self.children = []
        self.input = {}
        self.output = {}
        self.error = None
        self.duration = 0
        self.user_properties = {}
        self.metadata = {}
        self.start_time = 0
        self.end_time = 0
        self.call_value = None
        self.return_value = None
        self.context_set = False
        self.output_field = ""

    def log_event_with_data(self, event_data):
        # find all the keys in event_data that are not None
        # and add them to self
        for key, value in event_data.items():
            if value != None:
                # check if there's already a value for the key
                # if there is, don't overwrite it
                if getattr(self, key) == None:
                    setattr(self, key, value)
                else:
                    if isinstance(value, dict):
                        getattr(self, key).update(value)
                    else:
                        setattr(self, key, value)

        # check if "provider" and "endpoint" are in config
        if 'model' in self.metadata:
            self.config['model'] = self.metadata['model']
        if 'input' in self.metadata:
            if 'messages' in self.metadata['input']:
                self.input['chat_history'] = self.metadata['input']['messages']
            elif 'chat' in self.metadata['input']:
                self.input['chat_history'] = self.metadata['input']['chat']
        self.log_event()

    def end_session(self):
        end(session_id=self.session_id)

    def set_model_context(
        self,
        event_name,
        input,
        func,
        prompt_template="",
        chat_template=[],
        output_field="",
    ):
        # self.start_event()
        self.event_type = "model"
        self.event_name = event_name
        if chat_template != []:
            self.config['chat_template'] = chat_template
        if prompt_template != "":
            self.config['prompt_template'] = prompt_template
        self.input = input
        self.output_field = output_field
        if self.event_id == None:
            self.event_id = str(uuid.uuid4())
        self.context_set = True
        self.context_function_name = func.__name__
        self.context_file_name = inspect.getfile(func)
        return self.event_id

    def set_tool_context(
        self, event_name, description, func, config={}, output_field=""
    ):
        # self.start_event()
        self.event_type = "tool"
        self.event_name = event_name
        self.config = config
        self.config['description'] = description
        self.output_field = output_field
        if self.event_id == None:
            self.event_id = str(uuid.uuid4())
        self.context_set = True
        self.context_function_name = func.__name__
        self.context_file_name = inspect.getfile(func)
        # print("set tool context")
        # print(self.context_function_name)
        # print(self.context_file_name)
        return self.event_id

    def set_session_context(self, user_properties={}, metadata={}):
        self.user_properties = user_properties
        self.metadata = metadata

    def print_event(self):
        print("event")
        print("Event ID: " + self.event_id)
        print("Parent ID: " + self.parent_id)
        print("Event Type: " + self.event_type)
        print("Event Name: " + self.event_name)
        print("Config:")
        print(self.config)
        print("Input:")
        print(self.input)
        print("Output: " + self.output)
        print("Error: " + str(self.error))
        print("Duration: " + str(self.duration))
        print("Metadata:")
        print(self.metadata)
        print("User Properties:")
        print(self.user_properties)
        print("Children:")
        print(self.children)
        print("----")

    def tool(self, event_name, input={}, description="", config={}, output_field=""):
        self.start_event(event_type="tool")
        self.event_name = event_name
        self.config = config
        self.config['description'] = description
        self.input = input
        self.output_field = output_field

        self.trace_context_manager = HoneyHiveTraceContextManager(self)
        return self.trace_context_manager

    def model(
        self,
        event_name,
        input={},
        config={},
        description="",
        output_field="choices.0.message.content",
        prompt_template="",
        chat_template={},
    ):
        self.start_event(event_type="model")
        self.event_name = event_name
        self.config = config
        self.config['description'] = description
        self.input = input
        self.output_field = output_field
        if chat_template != {}:
            self.config['chat_template'] = chat_template
        if prompt_template != "":
            self.config['prompt_template'] = prompt_template

        self.trace_context_manager = HoneyHiveTraceContextManager(self)
        return self.trace_context_manager

    def add_openai_chat(
        self,
        event_name="openai_chat",
        config={},
        input={},
        description="",
        chat_template=[]
    ):
        self.start_event(event_type="model")
        self.event_name = event_name
        self.config = config
        self.config['description'] = description
        self.config['provider'] = "openai"
        self.config['endpoint'] = "chat"
        self.input = input
        self.output_field = "choices.0.message"
        if chat_template != {}:
            self.config['chat_template'] = chat_template

        self.trace_context_manager = HoneyHiveTraceContextManager(self)
        return self.trace_context_manager

    def completion_openai(
        self,
        event_name,
        input,
        config={},
        description="",
        output_field="",
        prompt_template="",
    ):
        self.start_event(event_type="model")
        self.event_name = event_name
        self.config = config
        self.config['description'] = description
        self.config['provider'] = "openai"
        self.config['endpoint'] = "completion"
        self.input = input
        self.output_field = output_field
        if prompt_template != "":
            self.config['prompt_template'] = prompt_template

        self.trace_context_manager = HoneyHiveTraceContextManager(self)
        return self.trace_context_manager

__all__ = ["HoneyHiveTracer"]
