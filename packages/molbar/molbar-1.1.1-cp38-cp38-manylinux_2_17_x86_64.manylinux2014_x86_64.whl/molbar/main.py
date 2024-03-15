import sys
import os
import json
from molbar.helper.debug import _get_debug_path, _mkdir_debug_path
from molbar.helper.parser import MolParser
from molbar.helper.printer import Printer
from molbar.barcode import get_molbar_from_file, get_molbars_from_files, idealize_structure_from_file

def main() -> None:
    """
    Main function for molbar. Parses arguments and calls the appropriate functions.
    """

    # Parse arguments from commandline
    arguments = MolParser().return_arguments()

    if arguments["mode"] == "opt":

        _init_idealization(arguments)

    else:

        _init_barcode_calculation(arguments)

def _init_idealization(arguments) -> None:

    if len(arguments["files"]) > 1:

        raise NotImplementedError("Idealization of multiple files is not implemented yet.")

    result = idealize_structure_from_file(arguments["files"][0], return_data=arguments["data"], timing=arguments["time"], input_constraint=arguments["constraints"][0], write_trj=True)
 
    if arguments["data"]:

        debug_path = _get_debug_path(arguments["files"][0])

        with open(os.path.join(debug_path, "output.json"), "w") as f:

            json.dump(result[4], f, indent=4)

    n_atoms = result[3]
    energy = result[0]
    coordinates = result[1]
    elements = result[2]

    filepath = arguments["files"][0].replace(".xyz", "").replace(".mol", "").replace(".sdf", "").replace(".coord", "") + ".opt"

    Printer(n_atoms=n_atoms, energy=energy, coordinates=coordinates, elements=elements, path=filepath).print()

def _init_barcode_calculation(arguments) -> None:

    if len(arguments["files"]) == 1:

        if arguments["data"]:

            result = get_molbar_from_file(arguments["files"][0], return_data=arguments["data"], timing=arguments["time"], input_constraint=arguments["constraints"][0], mode=arguments["mode"], write_trj=True)

            barcode = result[0]

            debug_path = _get_debug_path(arguments["files"][0])
            
            if os.path.isdir(debug_path) == False:
                    
                _mkdir_debug_path(debug_path)

            with open(os.path.join(debug_path, "output.json"), "w") as f:

                json.dump(result[1], f, indent=4)

        else:

            barcode = get_molbar_from_file(arguments["files"][0], return_data=arguments["data"], timing=arguments["time"], input_constraint=arguments["constraints"][0], mode=arguments["mode"])

        if arguments["save"] == True:

            output = arguments["files"][0].replace(".xyz", ".mb").replace(".coord", ".mb").replace(".sdf", ".mb").replace(".mol", ".mb")

            with open(output, 'w') as output_file:

                print(barcode, file=output_file)

        else:

            print(barcode, file=sys.stdout)

    else:

        if arguments["data"]:

            results = get_molbars_from_files(arguments["files"], return_data=arguments["data"], threads=arguments["threads"], timing=arguments["time"], input_constraints=arguments["constraints"], progress=arguments["progress"], mode=arguments["mode"], write_trj=True)

            barcodes = [result[0] for result in results]

            for filename, result in zip(arguments["files"], results):

                debug_path = _get_debug_path(filename)

                if os.path.isdir(debug_path) == False:

                    _mkdir_debug_path(debug_path)

                with open(os.path.join(debug_path, "output.json"), "w") as f:

                    json.dump(result[1], f, indent=4)
    
        else:

            barcodes = get_molbars_from_files(arguments["files"], return_data=arguments["data"], threads=arguments["threads"], timing=arguments["time"], input_constraints=arguments["constraints"], progress=arguments["progress"], mode=arguments["mode"])

        if arguments["save"] == True:

            for filename, barcode in zip(arguments["files"], barcodes):

                output = filename.replace(".xyz", ".mb").replace(".coord", ".mb").replace(".sdf", ".mb").replace(".mol", ".mb")

                with open(output, 'w') as output_file:

                    print(barcode, file=output_file)

        else:

            for barcode in barcodes:

                print(barcode, file=sys.stdout)

    
if __name__ == '__main__':

    from molbar.io.filereader import FileReader

    n_atoms, coordinates, elements = FileReader("/Users/nilsvanstaalduinen/molbar/example/binol_m.xyz").read_file()



    main()
