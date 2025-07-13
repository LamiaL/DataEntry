import os

BASE_DIR = os.path.expanduser("~")
# Ensure the data folder exists
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
DATA_FOLDER = os.path.join(BASE_DIR, "data")

DB_PATH_USERS = os.path.join(DATA_FOLDER, "users.db")
DB_PATH = os.path.join(DATA_FOLDER, "data_inventaire.db")
DB_PATH_RH = os.path.join(DATA_FOLDER, "data_inventaire_RH.db")
DB_PATH_FIN = os.path.join(DATA_FOLDER, "data_inventaire_FIN.db")
DB_PATH_M = os.path.join(DATA_FOLDER, "data_inventaire_M.db")
DB_PATH_LISTES = os.path.join(DATA_FOLDER, "data_listes.db")

CSV_PATH = os.path.join(BASE_DIR, "data", "data_inventaire.csv")
CSV_PATH_M = os.path.join(BASE_DIR, "data", "data_inventairem.csv")
CSV_PATH_FIN = os.path.join(BASE_DIR, "data", "data_inventairerh.csv")
CSV_PATH_RH = os.path.join(BASE_DIR, "data", "data_inventairefin.csv")

TABLE_CONFIG = {
        "dataENVMTable": {
            "db_path": DB_PATH_M,
            "table_name": "entriesenvm",
            "fields": ["nameAgent", "boxCote", "boxNum", "strc","intl", "mois", "anne", "typeDoc", "cond", "comtr"],
            "template": "edit_envm.html",  
            "redirect": "dataenvm.dataenvm_view",
            "required_lists": ["structures2", "conditionnement"],
              "lists": [
            {"list_name": "structures2", "key": "list_values"},
            {"list_name": "conditionnement", "key": "list2_values"} ]
        },
        "dataFINTable": {
            "db_path": DB_PATH_FIN,
            "table_name": "entriesfin",
            "fields": ["nameAgent","typedoc","de","au", "boxNum","manque","rmq"],
            "template": "edit_fin.html",  
            "redirect": "dataenvfin.dataenvfin_view",
            "lists": [
            {"list_name": "type_doc", "key": "list_values"} ]
        },
        "dataRHTable": {
            "db_path": DB_PATH_RH,
            "table_name": "entriesrh",
            "fields": ["nameAgent","mtl","name","fname", "bday","fonction", "dent", "dsor", "motifdepart" , "boxNum" , "addTopo","rmq"],
            "template": "edit_rh.html",  
            "redirect": "dataenvrh.dataenvrh_view",
            "lists": [
            {"list_name": "motif_depart", "key": "list_values"} ]
        },
         "dataENVTable": {
            "db_path": DB_PATH,
            "table_name": "entries",
            "fields": ["nameAgent","boxNum" ,"strc","exr","intl" , "addTopo"],
            "template": "edit_env.html",  
            "redirect": "dataenv.dataenv_view",
            "lists": [
            {"list_name": "structures", "key": "list_values"} ]
        },
        "dataLSTTable": {
            "db_path": DB_PATH_LISTES,
            "table_name": "parameters",
            "fields": ["id","list_name" ,"value"],
        }
    }
