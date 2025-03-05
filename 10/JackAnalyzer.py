import sys
import os
import CompilationEngine


def main():
    # Terminate if not given exactly 1 input
    if len(sys.argv) != 2:
        print("Error: exactly one (1) .jack file or directory as input expected")
        sys.exit()

    file_name = sys.argv[1]

    # When receiving a file as input
    if os.path.isfile(file_name):

        # Terminate if given input is not .jack
        if os.path.splitext(file_name)[1] != '.jack':
            print("Error: input file should have the extension \".jack\"")
            sys.exit()

        # create XML output
        toXML(file_name)

        print("Translation completed!")
    
    # When receiving a directory as input
    elif (os.path.isdir(file_name)):
        files = os.listdir(file_name)
        files = [os.path.join(file_name, f)
                 for f in files if os.path.splitext(f)[1] == '.jack']

        for f in files:
            toXML(f)
        print("Translation completed!")

    # Terminate if given input is not an existing file or directory
    else:
        print("Error: given input file doesn't exist")
        sys.exit()


def toXML(file_name):
    # create the output XML file
    outpath = os.path.abspath(file_name)[:-4]+'xml'
    
    # If ouput file exists, overwrite it
    if os.path.isfile(outpath):
        os.remove(outpath)
    
    engine = CompilationEngine.CompilationEngine(file_name, outpath)


if __name__ == '__main__':
    main()
