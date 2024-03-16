import GEOparse
import urllib.request
from tqdm import tqdm
import pandas as pd
import os
import logging
import sys

class GEOMetadataDownloader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.INFO)

    def download_geo_metadata(self, acc_file):
        all_family_dfs = []

        folder_name = "family_files"
        os.makedirs(folder_name, exist_ok=True)
        logging.basicConfig(filename="meta_log.txt",
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        with open(acc_file) as acc:
            for ac in acc:
                ac = ac.strip("\n")
                if not ac.startswith("GSE"):
                    continue
                
                digits = ac.replace("GSE", '')
                if len(digits) == 3:
                    nnnpart = "GSE"
                elif len(digits) == 4:
                    nnnpart = "GSE" + digits[0] 
                elif len(digits) == 5:
                    nnnpart = "GSE" + digits[:2]
                elif len(digits) == 6:
                    nnnpart = "GSE" + digits[:3]
                url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{nnnpart}nnn/{ac}/soft/{ac}_family.soft.gz'
                filename = os.path.join(folder_name, f'{ac}_family.soft.gz')

                if os.path.exists(filename):
                    try:
                        gse = GEOparse.get_GEO(filepath=filename)
                        if hasattr(gse, 'phenotype_data') and gse.phenotype_data is not None:
                            family_df = pd.DataFrame(gse.phenotype_data)
                            all_family_dfs.append(family_df)
                        else:
                            self.logger.warning(f"No phenotype information found for {ac}. Skipping.")
                    except Exception as parse_error:
                        self.logger.error(f"Error parsing {filename}: {parse_error}")
                else:
                    try:
                        with tqdm(unit="B", 
                                unit_scale=True, 
                                unit_divisor=1024, 
                                miniters=1,
                                desc=f"Downloading {filename}") as t:
                            urllib.request.urlretrieve(url, 
                                        			   filename,
                                        			   reporthook=lambda blocknum, 
                                        			   blocksize, 
                                        			   totalsize: t.update(blocksize))
                        
                        try:
                            gse = GEOparse.get_GEO(filepath=filename)
                            if hasattr(gse, 'phenotype_data') and gse.phenotype_data is not None:
                                family_df = pd.DataFrame(gse.phenotype_data)
                                all_family_dfs.append(family_df)
                            else:
                                self.logger.warning(f"No phenotype information found for {ac}. Skipping.")
                        except Exception as parse_error:
                            self.logger.error(f"Error parsing {filename}: {parse_error}")

                    except Exception as download_error:
                        self.logger.error(f"Error downloading {filename}: {download_error}")

        if all_family_dfs:
            combined_df = pd.concat(all_family_dfs, ignore_index=True)
            
            for type_value in combined_df['type'].unique():
                type_folder = os.path.join("result", type_value)
                os.makedirs(type_folder, exist_ok=True)
                
                type_df = combined_df[combined_df['type'] == type_value]
                type_df.to_excel(os.path.join(type_folder, f"metadata_{type_value}.xlsx"), index=False)
                
                self.logger.info(f"Metadata for type {type_value} saved to metadata_{type_value}.xlsx")
                
        else:
            self.logger.warning("No DataFrames available for concatenation.")


