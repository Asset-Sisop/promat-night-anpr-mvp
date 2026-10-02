from app.plate_format import normalize_rk_plate,is_valid_rk_plate

def test_valid(): assert normalize_rk_plate('123ABC01')=='123ABC01'
def test_spaces(): assert normalize_rk_plate('123 ABC 01')=='123ABC01'
def test_confusion(): assert normalize_rk_plate('1234BC01') is not None
def test_invalid(): assert not is_valid_rk_plate('12ABC01')
