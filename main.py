
from scripts.eodc import eodc_script
from scripts.eurac import eurac_script
from scripts.mundialis import mundialis_script
from scripts.sinergise import sinergise_script
from scripts.vito import vito_script
from scripts.wwu_gee import wwu_gee_script

backends = [
    {
        "name": "EODC",
        "data": ['L1C']
    },
    {
        "name": "EURAC",
        "data": ['L1C', 'L2A']
    },
    {
        "name": "Mundialis",
        "data": ['L1C']
    },
    {
        "name": "Sinergise",
        "data": ['L1C']
    },
    {
        "name": "VITO",
        "data": ['L1C', 'L2A']
    },
    {
        "name": "WWU_GEE",
        "data": ['L1C', 'L2A']
    }
]

for backend in backends:
    for data_item in backend['data']:
        print('Processing job from backend:', backend['name'], "-", data_item, "of", backend['data'])
        
        output_filename = f"results/min-evi_{backend['name']}_{data_item}.tif"
        if backend['name'] == 'EODC':            
            eodc_script(output_filename)
        elif backend['name'] == 'EURAC':            
            eurac_script(data_item, output_filename)
        elif backend['name'] == 'Mundialis':            
            mundialis_script(output_filename)
        elif backend['name'] == 'Sinergise':            
            sinergise_script(output_filename)
        elif backend['name'] == 'VITO':            
            vito_script(data_item, output_filename)
        elif backend['name'] == 'WWU_GEE':
            output_filename = output_filename.replace('.tif', '.png')
            wwu_gee_script(data_item, output_filename)
        
    print('\n')
