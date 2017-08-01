from __future__ import print_function
from __future__ import division

import argparse
import json
import os
import re
import sys

# replace with a direct Hermes parser
import wdl.parser

class wdltoil:

    def __init__(self, wdl_filename, secondary_filename):

        self.output_file = '/home/lifeisaboutfishtacos/Desktop/wdl-works/flow.py'

        self.module_list = ['from toil.job import Job',
                            'import subprocess']

        self.command_number = 0

        self.vars_from_2nd_file_dict = {}
        self.def_declarations_dict = {}

    def dict_from_YML(self, YML_file):
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

    def create_modules(self, module_list):
        module_portion = ''
        for module in self.module_list:
            module_portion = module_portion + str(module)
            module_portion = module_portion + '\n'
        return module_portion

    def create_definitions(self, formatted_WDL):
        ast = wdl.parser.parse(formatted_WDL).ast()
        # print(ast.dumps(indent=2))

        # Find all 'Task' ASTs
        tasks = wdl.find_asts(ast, 'Task')
        def_section = ''
        for task in tasks:
            next_definition = self.parse_task(task)
            def_section = def_section + next_definition
        return def_section

    def create_main(self):
        main_string = '\n\n\nif __name__=="__main__":' + \
                      '\n    options = Job.Runner.getDefaultOptions("./toilWorkflowRun")' + \
                      '\n    options.logLevel = "INFO"' + \
                      '\n    Job.Runner.startToil(job0, options)'
        return main_string

    def create_jobs(self, formatted_WDL):
        ast = wdl.parser.parse(formatted_WDL).ast()
        # print(ast.dumps(indent=2))

        # Find all 'Workflow' ASTs
        workflows = wdl.find_asts(ast, 'Workflow')
        job_section = ''
        for workflow in workflows:
            next_workflow = self.parse_workflow(workflow)
        #     job_section = job_section + next_job
        # return job_section
        return ''

    def parse_workflow(self, workflow):

        # CURRENTLY WORKING ON

        job_string = ''
        # print(workflow.attr("body"))

        for i in workflow.attr("body"):
            if i.name == "Declaration":
                if isinstance(i.attr("type"), wdl.parser.Terminal):
                    var_type = i.attr("type").source_string
                elif isinstance(i.attr("type"), wdl.parser.Ast):
                    var_type = i.attr("type").attributes["name"].source_string
                # print(var_type)
                var_name = i.attr("name").source_string
                # print(var_name)


        # context
        # for i in workflow.attr("body"):
        #     print('\n')
        #     print(i.attributes)
        #     try:
        #         print('type: ' + str(i.attributes['type'].source_string))
        #     except:
        #         pass
        #     try:
        #         print('name: ' + str(i.attributes['name'].source_string))
        #     except:
        #         pass
        #     try:
        #         print('task: ' + str(i.attributes['task'].source_string))
        #     except:
        #         pass



    def parse_task(self, task):

        task_name = task.attributes["name"].source_string

        # begin function header
        definition_string = ''
        definition_string = definition_string + '\n\ndef ' + str(task_name) + '(job, '

        # declarations
        for i in task.attr("declarations"):
            if isinstance(i.attr("type"), wdl.parser.Terminal):
                var_type = i.attr("type").source_string
            elif isinstance(i.attr("type"), wdl.parser.Ast):
                var_type = i.attr("type").attributes["name"].source_string
            var_name = i.attr("name").source_string

            # write declared variables into function header
            definition_string = definition_string + var_name + ', '

            # save declared variables and types for later
            var_tuple = (var_name, var_type)
            self.def_declarations_dict.setdefault(task_name, []).append(var_tuple)

        # end function header
        definition_string = definition_string + '):'


        # commandline scripts
        for i in task.attr("sections"):
            if i.name == "RawCommand":
                # first_command_var = 0
                full_command = ''
                command_input = ''
                command_string = ''
                for code_snippet in i.attributes["parts"]:
                    if isinstance(code_snippet, wdl.parser.Terminal):
                        command_var = code_snippet.source_string
                    if isinstance(code_snippet, wdl.parser.Ast):
                        command_var = "{" + code_snippet.attributes["expr"].source_string + "}"
                    command_var = command_var.replace('\n', '').replace(' \ ', '')
                    full_command = full_command + command_var

                command_var_list = full_command.split()

                vars =[]
                corrected_vars = []
                corrected_var = ''
                for command in command_var_list:
                    not_string = False
                    for letter in command:
                        if letter == '{':
                            not_string = True
                            if command_string != '':
                                command_string = "'" + command_string + "'"
                                vars.append(command_string)
                                command_string = ''
                                command_input = ''
                        if letter == '}':
                            not_string = False
                            if command_input != '':
                                vars.append(command_input)
                                command_string = ''
                                command_input = ''

                        if (not_string is True) and (letter != '}') and (letter != '{'):
                            command_input = command_input + letter
                        if (not_string is False) and (letter != '}') and (letter != '{'):
                            command_string = command_string + letter

                    if command_string != '':
                        command_string = "'" + command_string + "'"
                        vars.append(command_string)
                        command_string = ''
                        command_input = ''
                    if command_input != '':
                        vars.append(command_input)
                        command_string = ''
                        command_input = ''

                    for each_var in vars:
                        corrected_var = corrected_var + each_var + ' + '
                    vars = []
                    corrected_var = corrected_var[:-3]
                    corrected_vars.append(corrected_var)
                    corrected_var = ''

                command_var_decl_list = []
                for v in corrected_vars:
                    command_var_decl = 'command' + str(self.command_number)
                    command_var_declaration = command_var_decl + ' = ' + v
                    definition_string = definition_string + '\n    ' + command_var_declaration
                    command_var_decl_list.append(command_var_decl)
                    self.command_number = self.command_number + 1

            if i.name == "Outputs":
                # seems really redundant; will implement when it has a use
                pass

        definition_string = definition_string + '\n\n    subprocess.check_call(['
        for command_var in command_var_decl_list:
            definition_string = definition_string + str(command_var) + ', '
        definition_string = definition_string + '])\n'
        definition_string = definition_string + '    job.fileStore.logToMaster('
        definition_string = definition_string + "'"
        definition_string = definition_string + str(task_name)
        definition_string = definition_string + "')\n\n"

        return definition_string

        # if isinstance(task, wdl.parser.Terminal):
        #     print(task)
        #     print('id: ' + str(task.id))
        #     print('str: ' + str(task.str))
        #     print('source_string: ' + str(task.source_string))
        #     print('resource: ' + str(task.resource))
        #     print('line: ' + str(task.line))
        #     print('col: ' + str(task.col))
        # else:
        #     print(task.name)
        #     print(task.attributes)
        #     for i in task.attr("declarations"):
        #         print(i.attributes)
        #         print(i.attr("type").str)
        #         print(i.attr("type").source_string)

    def write_python_file(self, module_section, def_section, job_section, main_section, output_file):
        file = open(output_file, 'w')
        file.write(module_section)
        file.write(def_section)
        file.write(job_section)
        file.write(main_section)
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
    # if args.secondary_file.endswith('.json'):
    #     w.dict_from_JSON(args.secondary_file)
    # elif args.secondary_file.endswith('.yml'):
    #     w.dict_from_YML(args.secondary_file)
    # else:
    #     print('Unsupported Secondary File Type.  Please specify json or yml.')
    ##############################################################################

    formatted_WDL = w.format_WDL_code(wdl_file_path)

    module_section = w.create_modules(w.module_list)
    def_section    = w.create_definitions(formatted_WDL)
    job_section    = w.create_jobs(formatted_WDL)
    main_section    = w.create_main()

    w.write_python_file(module_section, def_section, job_section, main_section, w.output_file)

if __name__ == '__main__':
    main()

