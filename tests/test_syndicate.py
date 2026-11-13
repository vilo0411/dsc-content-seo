import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('syndicate',Path(__file__).resolve().parents[1]/'scripts/syndicate.py')
s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)

class MergeTests(unittest.TestCase):
    def test_date_roundtrip(self):
        self.assertEqual(s.date_from_serial(s.date_to_serial('2026-11-10')),'2026-11-10')
        self.assertEqual(s.date_to_serial(''),'')
        self.assertEqual(s.date_from_serial(''),'')
        row={k:'' for k in s.FIELDS}; row.update(id='date-test',posted_at='2026-11-10')
        encoded=s.sheet_row(row)
        self.assertIsInstance(encoded[s.FIELDS.index('posted_at')],int)
        self.assertEqual(s.from_sheet_row(s.FIELDS,encoded),row)
    def test_remote_change(self):
        b={'a':{'id':'a','status':'Draft'}}
        r,c=s.merge(b,b,{'a':{'id':'a','status':'Approved'}})
        self.assertEqual(r['a']['status'],'Approved'); self.assertFalse(c)
    def test_conflict(self):
        _,c=s.merge({'a':{'id':'a','status':'Draft'}},{'a':{'id':'a','status':'Posted'}},{'a':{'id':'a','status':'Skipped'}})
        self.assertEqual(c[0]['field'],'status')
    def test_missing_row_is_not_delete(self):
        b={'a':{'id':'a','status':'Draft'}}
        r,c=s.merge(b,b,{})
        self.assertEqual(r['a']['status'],'Draft'); self.assertFalse(c)
    def test_repeat_is_idempotent(self):
        b={'a':{'id':'a','status':'Approved'}}
        r,c=s.merge(b,b,b)
        again,c2=s.merge(r,r,r)
        self.assertEqual(r,again); self.assertFalse(c+c2)

if __name__=='__main__': unittest.main()
