def hello_world():
    print("therey")

def gen_data_dict():
    from sdmc_adhoc_processing.generate_dict import *

    if os.path.exists(output_dir + data_dict_fname):
        edit_existing_dict()
    else:
        build_brand_new_dict()
