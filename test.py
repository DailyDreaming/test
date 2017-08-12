from __future__ import print_function
from __future__ import division

import argparse
import json
import os
import re
import sys
import collections
import subprocess

# replace with a direct Hermes parser
import wdl.parser

class wdltoil:

    def __init__(self, wdl_filename, *args):

        self.output_file = '/home/lifeisaboutfishtacos/Desktop/wdl-works/wdl4.py'

        self.module_list = ['from toil.job import Job',
                            'from toil.common import Toil',
                            'import subprocess',
                            'import os']

        # from JSON or YML
        self.vars_from_2nd_file_dict = {}
        # holds task skeletons
        self.tasks_dictionary = {}
        # holds workflow structure
        self.jobs_dictionary = {}
        # array containing [(#, job), (#, job)... , (etc.)]
        self.function_order = []
        # dictionary of the arrays given to each function
        self.saved_scatter_input_vars = {}

        self.tsv_variables = {}
        self.output_variables = {}

        self.output_var_map = {}

        self.variable_map = []
        self.save_mapped_vars = []

        self.output_filename_number = 0
        self.output_def_number = 0
        self.sample_number = 0
        self.command_number = 0
        self.task_number = 0
        self.task_priority = 0

        self.wdl_file = wdl_filename
        self.secondary_file = args[0].secondary_file

    def make_tsv_array(self, tsv_filepath):
        tsv_array = []
        with open(tsv_filepath) as data_file:
            samples = data_file.readlines()
            for s in samples:
                s = s.replace('\n', '')
                data = s.split('\t')
                tsv_array.append(data)
        return(tsv_array)

    def dict_from_YML(self, YML_filepath):
        # write this
        pass

    def dict_from_JSON(self, JSON_file):
        with open(JSON_file) as data_file:
            data = json.load(data_file)
        for d in data:
            d_list = d.split('.')
            self.vars_from_2nd_file_dict[d_list[-1]] = data[d]

    def format_WDL_code(self, wdl_file):
        processed_WDLcode = ''
        for line in open(wdl_file):
            processed_WDLcode = processed_WDLcode + line
        return processed_WDLcode

    def write_modules(self, module_list):
        module_portion = ''
        for module in self.module_list:
            module_portion = module_portion + str(module)
            module_portion = module_portion + '\n'
        module_portion = module_portion + '\n\n'
        return module_portion

    def create_definitions(self, formatted_WDL):
        ast = wdl.parser.parse(formatted_WDL).ast()
        tasks = wdl.find_asts(ast, 'Task')
        for task in tasks:
            self.parse_task(task)

    def write_main(self):
        main_string = '\n\n\nif __name__=="__main__":' + \
                      '\n    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")' + \
                      '\n    options.logLevel = "DEBUG"' + \
                      '\n    with Toil(options) as toil:'
        return main_string

    def create_jobs(self, formatted_WDL):
        ast = wdl.parser.parse(formatted_WDL).ast()
        # print(ast.dumps(indent=2))
        workflows = wdl.find_asts(ast, 'Workflow')
        for workflow in workflows:
            self.parse_workflow(workflow)

    def parse_workflow_declaration(self, i):
        var_map = {}
        tsv = False
        # come back to add infinite depth subtypes (e.g. Array[Array[Array[rabbithole]]]...)
        if isinstance(i.attr("type"), wdl.parser.Terminal):
            var_type = i.attr("type").source_string
        elif isinstance(i.attr("type"), wdl.parser.Ast):
            var_type = i.attr("type").attributes["name"].source_string
        var_name = i.attr("name").source_string

        # check if any wdl functions are called to modify this variable in situ
        # only read_tsv currently supported
        tsv_array = []
        if i.attr("expression"):
            wdl_function_called = i.attr("expression").attributes['name'].source_string
            if wdl_function_called == 'read_tsv':
                # get all params for 'read_tsv'
                # expecting one file name pointing to a path in the JSON/YML secondary file
                for j in i.attr("expression").attributes['params']:
                    filename = j.source_string
                    tsv_filepath = self.vars_from_2nd_file_dict[filename]
                    tsv_array = self.make_tsv_array(tsv_filepath)
                    tsv = True

        if var_name in self.vars_from_2nd_file_dict:
            var_value = self.vars_from_2nd_file_dict[var_name]
        # deal with arrays other than tsv files
        elif var_type == 'Array':
            pass
        else:
            print('Variable in workflow declarations not found in secondary file.')
            var_value = ''

        if tsv:
            var_map['type'] = var_type
            var_map['value'] = tsv_array
        else:
            var_map['type'] = var_type
            var_map['value'] = var_value

        return var_name, var_map

    def parse_workflow_job(self, i):
        io_map = {}

        if i.attributes['body']:
            if i.attributes['body'].attributes['io']:
                for g in i.attributes['body'].attributes['io']:
                    for k in g.attributes['map']:
                        if isinstance(k.attributes['key'], wdl.parser.Terminal):
                            key_name = k.attributes['key'].source_string
                        if isinstance(k.attributes['value'], wdl.parser.Terminal):
                            value_name = k.attributes['value'].source_string
                            value_type = k.attributes['value'].str
                        if isinstance(k.attributes['key'], wdl.parser.Ast):
                            # never used in GATK tutorials; only a stub for later implementation
                            # print(k.attributes['key'].attributes)
                            pass
                        if isinstance(k.attributes['value'], wdl.parser.Ast):
                            if k.attributes['value'].attributes['rhs'].str == 'integer':
                                output_variable = k.attributes['value'].attributes['rhs'].source_string
                                task = k.attributes['value'].attributes['lhs'].source_string
                                value_name = task + ' ' + output_variable
                                value_type = 'index_value'
                            elif k.attributes['value'].attributes['rhs'].str == 'identifier':
                                output_variable = k.attributes['value'].attributes['rhs'].source_string
                                task = k.attributes['value'].attributes['lhs'].source_string
                                value_name = task + ' ' + output_variable
                                value_type = 'output'
                            else:
                                print('Unsupported rhs type.')
                                output_variable = k.attributes['value'].attributes['rhs'].source_string
                                task = k.attributes['value'].attributes['lhs'].source_string
                                value_name = task + ' ' + output_variable
                                value_type = 'output'

                        io_map.setdefault(key_name, {})['name'] = value_name
                        io_map.setdefault(key_name, {})['type'] = value_type
        return(io_map)

    def parse_workflow(self, workflow):
        workflow_name = workflow.attr('name').source_string

        wf_declared_dict = {}
        for i in workflow.attr("body"):

            if i.name == "Declaration":
                var_name, var_map = self.parse_workflow_declaration(i)
                wf_declared_dict[var_name] = var_map
            self.jobs_dictionary.setdefault(workflow_name, {})['wf_declarations'] = wf_declared_dict

            if i.name == "Scatter":
                self.task_priority = self.task_priority + 1

                # name of iterator; e.g. 'sample'
                # also serves as a variable input in function for indexed variables; e.g. sample[0], sample[1], etc.
                scatter_counter = i.attributes['item'].source_string
                # name of collection to iterate over
                scatter_collection = i.attributes['collection'].source_string

                if scatter_collection in self.jobs_dictionary[workflow_name]['wf_declarations']:
                    if self.jobs_dictionary[workflow_name]['wf_declarations'][scatter_collection]['type'] == 'Array':
                        scatter_array = self.jobs_dictionary[workflow_name]['wf_declarations'][scatter_collection]['value']
                        for set_of_vars in scatter_array:
                            for j in i.attributes['body']:
                                self.task_number = self.task_number + 1
                                task_being_called = j.attributes['task'].source_string
                                if j.attributes['alias']:
                                    task_alias = j.attributes['alias'].source_string
                                else:
                                    task_alias = task_being_called
                                job = self.parse_workflow_job(j)
                                self.jobs_dictionary.setdefault((self.task_priority, self.task_number, task_being_called, task_alias), {})['job_declarations'] = job
                                self.saved_scatter_input_vars.setdefault((self.task_priority, self.task_number, task_being_called, task_alias), {})[scatter_counter] = set_of_vars
                    else:
                        print('Scatter failed.  Scatter collection is not an array.')
                else:
                    print('Scatter failed.  Scatter collection not found in jobs_dictionary.')

            if i.name == "Call":
                self.task_priority = self.task_priority + 1
                self.task_number = self.task_number + 1
                task_being_called = i.attributes['task'].source_string
                if i.attributes['alias']:
                    task_alias = i.attributes['alias'].source_string
                else:
                    task_alias = task_being_called
                job = self.parse_workflow_job(i)
                self.jobs_dictionary.setdefault((self.task_priority, self.task_number, task_being_called, task_alias), {})['job_declarations'] = job

    def parse_task(self, task):

        task_name = task.attributes["name"].source_string

        # declarations
        declaration_dict = {}
        declaration_array = []
        for i in task.attr("declarations"):
            var_name = i.attr("name").source_string
            if isinstance(i.attr("type"), wdl.parser.Terminal):
                var_type = i.attr("type").source_string
            elif isinstance(i.attr("type"), wdl.parser.Ast):
                var_type = i.attr("type").attributes["name"].source_string
            declaration_dict[var_name] = var_type
            var_tuple = (var_name, var_type)
            declaration_array.append(var_tuple)
        self.tasks_dictionary.setdefault(task_name, {})['inputs'] = declaration_dict
        self.tasks_dictionary.setdefault(task_name, {})['ordered_inputs'] = declaration_array

        # sections (commandline entries; output filenames)
        additional_conditions_list = []
        command_array = []
        for i in task.attr("sections"):

            # commandline entries section
            if i.name == "RawCommand":
                for code_snippet in i.attributes["parts"]:
                    if isinstance(code_snippet, wdl.parser.Terminal):
                        command_var = code_snippet.source_string
                        command_type = 'normal_string'
                    if isinstance(code_snippet, wdl.parser.Ast):
                        command_var = code_snippet.attributes["expr"].source_string
                        command_type = 'variable'
                        if code_snippet.attributes['attributes']:
                            for additional_conditions in code_snippet.attributes['attributes']:
                                keyword_for_a_command = additional_conditions.attributes['key'].source_string
                                some_value_used_by_the_keyword = additional_conditions.attributes['value'].source_string
                                additional_conditions_list.append((keyword_for_a_command, some_value_used_by_the_keyword))
                    command_var = command_var.replace('\n', '').replace(' \ ', '')
                    command_array.append((command_var, command_type, additional_conditions_list))
                    additional_conditions_list = []

            self.tasks_dictionary.setdefault(task_name, {})['raw_commandline'] = command_array

            # output filenames section
            output_dict = {}
            output_vars_dict = {}
            if i.name == "Outputs":
                for j in i.attributes['attributes']:
                    if j.name == 'Output':
                        var_type = j.attributes['type'].source_string
                        var_name = j.attributes['var'].source_string
                        var_value = j.attributes['expression'].source_string
                        output_vars_dict['type'] = var_type
                        output_vars_dict['value'] = var_value
                        output_dict[var_name] = output_vars_dict

            self.tasks_dictionary.setdefault(task_name, {})['outputs'] = output_dict

    def return_one_job_per_priority(self):
        job_set = []
        for i in range(len(self.jobs_dictionary)):
            for job in self.jobs_dictionary:
                if i == job[0]:
                    job_set.append(job)
                    break
        return(job_set)

    def write_jobs(self):
        job_section = ''

        # write out the scatter variable declarations
        job_section = job_section + '\n        # Scatter Variables\n'
        for tsv_vars in self.saved_scatter_input_vars:
            for var in self.saved_scatter_input_vars[tsv_vars]:
                i = 0
                for v in self.saved_scatter_input_vars[tsv_vars][var]:
                    sample_var = var + str(i) + '_' + str(tsv_vars[1])
                    i = i + 1
                    if os.path.isfile(v):
                        filename = v.split('/')
                        filename = filename[-1]
                        job_section = job_section + '        ' + sample_var + ' = toil.importFile("file://' + v + '")\n'
                        job_section = job_section + '        ' + sample_var + '_og = "' + filename + '"\n'
                    elif isinstance(v, (str, unicode)):
                        job_section = job_section + '        ' + sample_var + ' = "' + v + '"\n'
                    else:
                        job_section = job_section + '        ' + sample_var + ' = ' + v + '\n'

        # write out the JSON/YML file declarations
        job_section = job_section + '\n        # JSON/YML Variables\n'
        for vars in self.vars_from_2nd_file_dict:
            v = self.vars_from_2nd_file_dict[vars]
            if os.path.isfile(v):
                filename = v.split('/')
                filename = filename[-1]
                job_section = job_section + '        ' + vars + ' = toil.importFile("file://' + v + '")\n'
                job_section = job_section + '        ' + vars + '_og = "' + filename + '"\n'
            elif isinstance(v, (str, unicode)):
                job_section = job_section + '        ' + vars + ' = "' + v + '"\n'
            else:
                job_section = job_section + '        ' + vars + ' = ' + v + '\n'

        # write out any output filenames that need to be preserved through the run
        job_section = job_section + '\n        # Output Variables\n'
        for outputs in self.output_var_map:
            for file in self.output_var_map[outputs][0]:
                if file[1] == 'File':
                    split_filename = self.output_var_map[outputs][1].split('}')
                    filename = split_filename[-1]
                    filename = str(file[0]) + filename
                    job_section = job_section + '        ' + file[0] + '_og = "' + filename + '"\n'
                else:
                    pass

        job_section = job_section + '\n        job0 = Job.wrapJobFn(initialize_jobs)\n'

        job_declaration_dict = self.get_job_wrappers()
        for job_wrap in job_declaration_dict:
            job_section = job_section + '        ' + job_wrap + ' = Job.wrapJobFn('
            for var in job_declaration_dict[job_wrap]:
                job_section = job_section + var + ', '
            job_section = job_section[:-2]
            job_section = job_section + ')\n'

        for priority in range(self.task_priority + 1):
            for job_declaration in self.jobs_dictionary:
                if isinstance(job_declaration, (list, tuple)):
                    if job_declaration[0] == priority:
                        job_section = job_section + '        job0.addChild(job' + str(job_declaration[1]) + ')\n'
            job_section = job_section + '\n        job0 = job0.encapsulate()\n'
        job_section = job_section[:-34]
        job_section = job_section + '        toil.start(job0)'

        return job_section

    def get_job_wrappers(self):

        job_dict = {}

        for job_declaration in self.jobs_dictionary:
            job_array = []
            if isinstance(job_declaration, (list, tuple)):
                for job_map in self.variable_map:
                    if job_declaration[0] == job_map[0][0]:
                        # job_array.append(job_declaration[3])
                        for variable_input in job_map[2]:
                            if variable_input[1] == 'File':
                                if variable_input[2] == 'index_value':
                                    write_var = variable_input[3] + '_' + str(job_declaration[1])
                                    job_array.append(write_var)
                                    write_var = variable_input[3] + '_' + str(job_declaration[1]) + '_og'
                                    job_array.append(write_var)
                                elif variable_input[2] == 'output':
                                    write_var = variable_input[3]
                                    job_array.append(write_var)
                                    write_var = variable_input[0] + '_og'
                                    job_array.append(write_var)
                                else:
                                    write_var = variable_input[3]
                                    job_array.append(write_var)
                                    write_var = variable_input[3] + '_og'
                                    job_array.append(write_var)
                            else:
                                if variable_input[2] == 'index_value':
                                    write_var = variable_input[3] + '_' + str(job_declaration[1])
                                    job_array.append(write_var)
                                else:
                                    write_var = variable_input[3]
                                    job_array.append(write_var)
                    fresh_job_array = []
                    fresh_job_array.append(job_declaration[3])
                    fresh_job_array.extend(job_array)
                    job_dict['job' + str(job_declaration[1])] = fresh_job_array

        ordered_job_dict = collections.OrderedDict(sorted(job_dict.items(), key=lambda t: t[0]))

        return ordered_job_dict

    def write_functions(self):

        # write default function for running jobs
        fn_section = "def initialize_jobs(job):\n    job.fileStore.logToMaster('initialize_jobs')\n"

        # iterate with jobs_dictionary
        # get default variables list from tasks_dictionary
        # map and replace variables from job_dictionary

        list_of_jobs_to_write = self.return_one_job_per_priority()

        for job in list_of_jobs_to_write:
            job_priority = job[0]
            job_number = job[1]
            job_task_reference = job[2]
            job_alias = job[3]

            # write the function header
            fn_section = fn_section + '\n\ndef ' + job_alias + '(job, '
            job_declaration_array = self.get_job_declarations(job, job_priority, job_number, job_task_reference, job_alias)
            for job_declaration in job_declaration_array:
                job_declaration_name = job_declaration[0]
                job_declaration_type = job_declaration[1]
                if job_declaration_type == 'File':
                    fn_section = fn_section + job_declaration_name + ', ' + job_declaration_name + '_og, '
                else:
                    fn_section = fn_section + job_declaration_name + ', '
            fn_section = fn_section[:-2]
            fn_section = fn_section + '):\n'

            fn_section = fn_section + '    job.fileStore.logToMaster("' + job_alias + '")\n'
            fn_section = fn_section + '    tempDir = job.fileStore.getLocalTempDir()\n\n'

            # write out File declarations
            for job_declaration in job_declaration_array:
                job_declaration_name = job_declaration[0]
                job_declaration_type = job_declaration[1]
                if job_declaration_type == 'File':
                    fn_section = fn_section + '    ' + job_declaration_name + '_filepath = os.path.join(tempDir, ' + job_declaration_name + '_og)\n'
                    fn_section = fn_section + '    ' + job_declaration_name + ' = job.fileStore.readGlobalFile(' + job_declaration_name + ', userPath=' + job_declaration_name + '_filepath)\n'

            fn_section = fn_section + '\n'

            # write out commandline keywords
            commandline_array = self.get_commandline_array(job)
            command_var_decl_array = []
            for command in commandline_array:
                command_var_decl = 'command' + str(self.command_number)
                fn_section = fn_section + '    ' + command_var_decl + ' = ' + command + '\n'
                self.command_number = self.command_number + 1
                command_var_decl_array.append(command_var_decl)

            # write the check_call line to run the commandline keywords in a chain
            fn_section = fn_section + '\n    subprocess.check_call(['
            for command in command_var_decl_array:
                fn_section = fn_section + command + ', '
            fn_section = fn_section[:-2]
            fn_section = fn_section + '])\n\n'

            # write the outputs for the definition to return
            files_to_return = []
            for output in self.tasks_dictionary[job[2]]['outputs']:
                output_name = self.tasks_dictionary[job[2]]['outputs'][output]['value']
                formatted_output_filename = self.parse_raw_output(job, output_name)
                output_filename = 'output_file' + str(self.output_def_number)
                fn_section = fn_section + '    output_filename' + str(self.output_def_number) + " = " + formatted_output_filename + '\n'
                fn_section = fn_section + '    ' + output_filename + " = job.fileStore.writeGlobalFile(output_filename" + str(self.output_def_number) + ')\n'
                self.output_def_number = self.output_def_number + 1
                files_to_return.append(output_filename)
            fn_section = fn_section + '    return '
            for file in files_to_return:
                fn_section = fn_section + file + ', '
            fn_section = fn_section[:-2]

        return fn_section

    def parse_raw_output(self, job, some_string):
        # add support for 'sep'
        output_string = ''
        edited_string = some_string

        continue_loop = True
        while(continue_loop):
            index_start = edited_string.find('${')
            index_end = edited_string.find('}', index_start)

            stringword = edited_string[:index_start]
            if stringword:
                output_string = output_string + "'" + stringword + "' + "

            keyword = edited_string[index_start+2:index_end]
            term = self.get_mapped_terms(job, keyword)
            output_string = output_string + term[0][0] + " + "

            edited_string = edited_string[index_end+1:]
            if edited_string.find('${') == -1:
                continue_loop = False
                if edited_string:
                    output_string = output_string + "'" + edited_string + "' + "

        output_string = output_string[:-3]

        return output_string

    def get_mapped_terms(self, job, term):
        found_terms = ''
        for mapped_terms in self.save_mapped_vars:
            if job == mapped_terms[0]:
                if term == mapped_terms[1][0]:
                    found_terms = mapped_terms[2]
        if found_terms == '':
            print('Mapped term not found.')
        return found_terms

    def get_commandline_array(self, job):
        current_var = ''
        master_cmd_array = []
        super_array = []
        sub_array = []
        previous_left_separator = True
        previous_right_separator = True
        for var in self.variable_map:
            if job == var[0]:
                self.save_mapped_vars.append(var)

        for cmd in self.tasks_dictionary[job[2]]['raw_commandline']:
            cmd_name = cmd[0]
            cmd_type = cmd[1]
            cmd_optional = cmd[2]

            if cmd_optional:
                for option in cmd_optional:
                    if option[0] == 'sep':
                        mapped_terms = self.get_mapped_terms(job, cmd_name)
                        for name in mapped_terms:
                            if var[1] == 'String':
                                master_cmd_array.append("'" + name[0] + "'")
                                master_cmd_array.append("'" + option[1].strip() + "'")
                            else:
                                master_cmd_array.append(name[0])
                                master_cmd_array.append("'" + option[1].strip() + "'")
                        master_cmd_array = master_cmd_array[:-1]
                    else:
                        print('Unsupported and unknown cmd_option.')
            else:
                if cmd_type == 'normal_string':
                    left_separator = False
                    right_separator = False
                    if cmd_name.startswith(' '):
                        left_separator = True
                    if cmd_name.endswith(' '):
                        right_separator = True
                elif cmd_type == 'variable':
                    left_separator = False
                    right_separator = False
                else:
                    print('Unknown type found in commandline.')

                if left_separator and right_separator:
                    super_array.append(current_var)
                    subsub_array = self.clean_array(cmd_name)
                    for c in subsub_array:
                        if c != '':
                            sub_array.append("'" + c + "'")
                    super_array.extend(sub_array)
                    for c in super_array:
                        if c != '':
                            master_cmd_array.append(c)
                    super_array = []
                    sub_array = []
                    current_var = ''
                else:
                    if current_var == '':
                        if cmd_type == 'normal_string':
                            current_var = current_var + "'" + cmd_name.strip() + "'"
                        elif cmd_type == 'variable':
                            if self.get_mapped_terms(job, cmd_name):
                                current_var = current_var + self.get_mapped_terms(job, cmd_name)[0][0]
                            else:
                                current_var = current_var + cmd_name
                        else:
                            print('Unknown type found in commandline.')
                    else:
                        if cmd_type == 'normal_string':
                            current_var = current_var + " + '" + cmd_name.strip() + "'"
                        elif cmd_type == 'variable':
                            if self.get_mapped_terms(job, cmd_name):
                                current_var = current_var + " + " + self.get_mapped_terms(job, cmd_name)[0][0]
                            else:
                                current_var = current_var + cmd_name
                        else:
                            print('Unknown type found in commandline.')
        if current_var != '':
            master_cmd_array.append(current_var)
        return master_cmd_array

    def clean_array(self, cmd_name):
        append_to_me = []
        temp_string = ''
        record_spaces = False
        for char in cmd_name:
            if (char != ' ') and (char != '"') and (char != "'"):
                temp_string = temp_string + char
            elif (char == ' ') and (record_spaces is False):
                append_to_me.append(temp_string)
                temp_string = ''
            elif (char == ' ') and (record_spaces is True):
                temp_string = temp_string + char
            elif char == '"':
                record_spaces = not record_spaces
                append_to_me.append(temp_string)
                temp_string = ''
            elif char == "'":
                record_spaces = not record_spaces
                append_to_me.append(temp_string)
                temp_string = ''
            else:
                pass
        append_to_me.append(temp_string)
        return append_to_me

    def map_type_to_type(self, job, task_input_variable):
        input_variable_to_write = []
        new_type = task_input_variable[1]
        if task_input_variable[0] in self.jobs_dictionary[job]['job_declarations']:
            job_input_type = self.jobs_dictionary[job]['job_declarations'][task_input_variable[0]]['type']
            job_input_name = self.jobs_dictionary[job]['job_declarations'][task_input_variable[0]]['name']

            if job_input_type == 'identifier':
                input_variable_to_write.append((job_input_name, new_type, job_input_type, job_input_name))

            elif job_input_type == 'index_value':
                input_variable_to_write.append((job_input_name.split()[0] + job_input_name.split()[1], new_type, job_input_type, job_input_name.split()[0] + job_input_name.split()[1]))
                self.sample_number = self.sample_number + 1

            elif job_input_type == 'output':
                task_called = job_input_name.split()[0]
                output_filename = job_input_name.split()[1]

                # if name is an alias, get real name
                alias_called = task_called
                if task_called not in self.tasks_dictionary:
                    for tasks in self.jobs_dictionary:
                        if task_called == tasks[3]:
                            task_called = tasks[2]

                if output_filename in self.tasks_dictionary[task_called]['outputs']:
                    new_type = self.tasks_dictionary[task_called]['outputs'][output_filename]['type']
                    new_value = self.tasks_dictionary[task_called]['outputs'][output_filename]['value']
                else:
                    print("Error, could not find output filename in tasks dictionary.")
                num_of_output_vars = self.find_jobs_calling_this_task(job, alias_called)
                list_of_output_vars = []
                for job_number in num_of_output_vars:
                    list_of_output_vars.append((output_filename + str(job_number), new_type, job_input_type, 'job' + str(job_number) + '.rv()'))
                input_variable_to_write = list_of_output_vars
                self.output_var_map[task_input_variable[0]] = (list_of_output_vars, new_value, task_called, job)

            elif job_input_type == 'string':
                input_variable_to_write.append((task_input_variable[0], new_type, job_input_type, "'" + job_input_name + "'"))

        else:
            input_variable_to_write.append((task_input_variable[0], new_type, 'identifier', task_input_variable[0]))

        return input_variable_to_write

    def find_jobs_calling_this_task(self, job, alias_called):
        jobs_that_called_this_task = []
        for tasks in self.jobs_dictionary:
            # check to make sure tasks is a list here <----
            if tasks[0] <= job[0]:
                if alias_called == tasks[3]:
                    jobs_that_called_this_task.append(tasks[1])
        return jobs_that_called_this_task

    def get_job_declarations(self, job, job_priority, job_number, job_task_reference, job_alias):
        declarations_list = []

        # for each default variable from the task declaration
        for task_input_variable in self.tasks_dictionary[job_task_reference]['ordered_inputs']:
            input_variable_to_write = self.map_type_to_type(job, task_input_variable)
            self.variable_map.append((job, task_input_variable, input_variable_to_write))
            declarations_list.extend(input_variable_to_write)
        return declarations_list

    def write_python_file(self, module_section, fn_section, main_section, job_section, output_file):
        file = open(output_file, 'w')
        file.write(module_section)
        file.write(fn_section)
        file.write(main_section)
        file.write(job_section)
        file.close

def main():
    parser = argparse.ArgumentParser(description='Convert WDL to Toil')
    parser.add_argument('wdl_file', help='a WDL workflow or a directory with WDL files')
    parser.add_argument('secondary_file', help='secondary data file (json or yml)')
    parser.add_argument('--tsv', help='file with sample names for the scatter function')
    args = parser.parse_args()

    wdl_file_path = os.path.abspath(args.wdl_file)
    args.secondary_file = os.path.abspath(args.secondary_file)

    w = wdltoil(wdl_file_path, args)

    ##############################################################################
    # read secondary file; create dictionary to hold variables
    if args.secondary_file.endswith('.json'):
        w.dict_from_JSON(args.secondary_file)
    elif args.secondary_file.endswith('.yml'):
        w.dict_from_YML(args.secondary_file)
    else:
        print('Unsupported Secondary File Type.  Please specify json or yml.')
    ##############################################################################

    formatted_WDL = w.format_WDL_code(wdl_file_path)

    w.create_definitions(formatted_WDL)
    w.create_jobs(formatted_WDL)

    module_section = w.write_modules(w.module_list)
    fn_section = w.write_functions()
    main_section = w.write_main()
    job_section = w.write_jobs()

    # print('\n\n')
    # for each_task in w.tasks_dictionary:
    #     print(each_task)
    #     for each_section in w.tasks_dictionary[each_task]:
    #         print('    ' + str(each_section))
    #         for each_variable in w.tasks_dictionary[each_task][each_section]:
    #             print('        ' + str(each_variable))
    #
    # print('\n\n')
    # for each_task in w.jobs_dictionary:
    #     print(each_task)
    #     if 'wf_declarations' in w.jobs_dictionary[each_task]:
    #         print('    wf_declarations')
    #         for d in w.jobs_dictionary[each_task]['wf_declarations']:
    #             print('        ' + str(d))
    #     if 'job_declarations' in w.jobs_dictionary[each_task]:
    #         print('    job_declarations')
    #         for j in w.jobs_dictionary[each_task]['job_declarations']:
    #             print('        ' + str(j))
    #             for g in w.jobs_dictionary[each_task]['job_declarations'][j]:
    #                 print('            ' + g + ': ' + w.jobs_dictionary[each_task]['job_declarations'][j][g])
    #
    # print('\n\n')
    # for each_task in w.saved_scatter_input_vars:
    #     print(each_task)
    #     print(w.saved_scatter_input_vars[each_task])

    w.write_python_file(module_section, fn_section, main_section, job_section, w.output_file)

    subprocess.check_call(['python', w.output_file])

if __name__ == '__main__':
    main()
