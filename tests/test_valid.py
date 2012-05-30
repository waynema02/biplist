from biplist import *
import datetime
import os
from test_utils import *
import unittest

class TestValidPlistFile(unittest.TestCase):
    def setUp(self):
        pass
    
    def validateSimpleBinaryRoot(self, root):
        self.assertTrue(type(root) == dict, "Root should be dictionary.")
        self.assertTrue(type(root[b'dateItem']) == datetime.datetime, "date should be datetime")
        self.assertEqual(root[b'dateItem'], datetime.datetime(2010, 8, 19, 22, 27, 30, 385449), "dates not equal" )
        self.assertEqual(root[b'numberItem'], -10000000000000000, "number not of expected value")
        self.assertEqual(root[b'unicodeItem'], 'abc\u212cdef\u2133')
        self.assertEqual(root[b'stringItem'], b'Hi there')
        self.assertEqual(root[b'realItem'], 0.47)
        self.assertEqual(root[b'boolItem'], True)
        self.assertEqual(root[b'arrayItem'], [b'item0'])
        
    def testFileRead(self):
        try:
            result = readPlist(data_path('simple_binary.plist'))
            self.validateSimpleBinaryRoot(result)
        except NotBinaryPlistException as e:
            self.fail("NotBinaryPlistException: %s" % e)
        except InvalidPlistException as e:
            self.fail("InvalidPlistException: %s" % e)
    
    def testUnicodeRoot(self):
        result = readPlist(data_path('unicode_root.plist'))
        self.assertEqual(result, "Mirror's Edge\u2122 for iPad")
    
    def testEmptyUnicodeRoot(self):
        result = readPlist(data_path('unicode_empty.plist'))
        self.assertEqual(result, b"")
    
    def testSmallReal(self):
        result = readPlist(data_path('small_real.plist'))
        self.assertEqual(result, {b'4 byte real':0.5})
    
    def testKeyedArchiverPlist(self):
        """
        Archive is created with class like this:
        @implementation Archived
        ...
        - (void)encodeWithCoder:(NSCoder *)coder {
            [coder encodeObject:@"object value as string" forKey:@"somekey"];
        }
        @end
        
        Archived *test = [[Archived alloc] init];
        NSData *data = [NSKeyedArchiver archivedDataWithRootObject:test]
        ...
        """
        result = readPlist(data_path('nskeyedarchiver_example.plist'))
        self.assertEqual(result, {b'$version': 100000, 
            b'$objects': 
                [b'$null', 
                 {b'$class': Uid(3), b'somekey': Uid(2)}, 
                 b'object value as string', 
                 {b'$classes': [b'Archived', b'NSObject'], b'$classname': b'Archived'}
                 ], 
            b'$top': {b'root': Uid(1)}, b'$archiver': b'NSKeyedArchiver'})
        self.assertEqual("Uid(1)", repr(Uid(1)))
    
if __name__ == '__main__':
    unittest.main()
