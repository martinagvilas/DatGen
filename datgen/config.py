from pathlib import Path

## PATH
current_path = Path().parent.resolve()
if 'm_vilas' in str(current_path):
    ANNOT_PATH = Path(
        '/Users/m_vilas/uni/software_engineering/DatGen/datasets/annot'
    )
    IMGS_PATH = Path(
        '/Users/m_vilas/uni/software_engineering/DatGen/datasets/images'
    )
else:
    ANNOT_PATH = Path('../data/datgen_data/image_metas/annot')
    IMGS_PATH = Path('../data/datgen_data/image_metas/images')