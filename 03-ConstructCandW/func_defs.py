#-----------------------------------------------------------------
# pycparser: func_defs.py
#
# Using pycparser for printing out all the functions defined in a
# C file.
#
# This is a simple example of traversing the AST generated by
# pycparser.
#
# Copyright (C) 2008-2015, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file


# A simple visitor for FuncDef nodes that prints the names and
# locations of function definitions.
class FuncDefVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.nodes =[]
    def visit_FuncDef(self, node):
        #print('%s at %s' % (node.decl.name, node.decl.coord))
        self.nodes.append(node);


def show_func_defs(text):
    # Note that cpp is used. Provide a path to your own cpp or
    # make sure one exists in PATH.
    parser = c_parser.CParser()
    ast = parser.parse(text, filename='<none>')

    v = FuncDefVisitor()
    v.visit(ast)
    nodes = v.nodes;

    function_body = nodes[0].body
    print ('len =' ,function_body.NodeNum())
    # for decl in function_body.block_items:
    #     decl.show()
    # print ("\n \n")
    function_body = nodes[1].body
    print ('len =' , function_body.NodeNum())
    for decl in function_body.block_items:
        decl.show()


if __name__ == "__main__":
    text = r"""
    typedef int Node, Hash;

    void HashPrint(Hash* hash, void (*PrintFunc)(char*, char*))
    {
        unsigned int i;

        if (hash == NULL || hash->heads == NULL)
            return;

        for (i = 0; i < hash->table_size; ++i)
        {
            Node* temp = hash->heads[i];

            while (temp != NULL)
            {
                PrintFunc(temp->entry->key, temp->entry->value);
                temp = temp->next;
            }
        }
    }
    int main()
    {
        int x = 10;
        int y = 2;
        printf("%d", x+y);
        getch();
    }
    """

    show_func_defs(text)
