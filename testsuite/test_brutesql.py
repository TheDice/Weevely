from baseclasses import SimpleTestCase, conf
from tempfile import NamedTemporaryFile
import random, string
import sys, os
sys.path.append(os.path.abspath('..'))
import modules

class BruteSQL(SimpleTestCase):
    
    def _generate_wordlist(self):
        wordlist = [''.join(random.choice(string.ascii_lowercase) for x in range(random.randint(1,100))) for x in range(random.randint(1,200)) ]
        wordlist[random.randint(0,len(wordlist))] = conf['bruteforce_sql_pwd']
        return wordlist
        
    
    def test_brutesql(self):

        expected_match = [ conf['bruteforce_sql_user'], conf['bruteforce_sql_pwd'] ]

        self.assertEqual(self._res(':bruteforce.sql %s -wordlist "%s"' % (conf['bruteforce_sql_user'], str(self._generate_wordlist()))), expected_match)
        
        temp_path = NamedTemporaryFile(); 
        temp_path.write('\n'.join(self._generate_wordlist()))
        temp_path.flush() 
        
        self.assertEqual(self._res(':bruteforce.sql %s -wordfile "%s"' % (conf['bruteforce_sql_user'], temp_path.name)), expected_match)
        self.assertRegexpMatches(self._warn(':bruteforce.sql %s -wordfile "%sunexistant"' % (conf['bruteforce_sql_user'], temp_path.name)), modules.bruteforce.sql.WARN_NO_SUCH_FILE)
        self.assertRegexpMatches(self._warn(':bruteforce.sql %s' % (conf['bruteforce_sql_user'])), modules.bruteforce.sql.WARN_NO_WORDLIST)
        
        self.assertEqual(self._res(':bruteforce.sql %s -chunksize 1 -wordlist "%s"' % (conf['bruteforce_sql_user'], str(self._generate_wordlist()))), expected_match)
        self.assertEqual(self._res(':bruteforce.sql %s -chunksize 100000 -wordlist "%s"' % (conf['bruteforce_sql_user'], str(self._generate_wordlist()))), expected_match)
        self.assertEqual(self._res(':bruteforce.sql %s -chunksize 0 -wordlist "%s"' % (conf['bruteforce_sql_user'], str(self._generate_wordlist()))), expected_match)
        
        # TODO: add -startline tests, wrong user/hostname, other dbms check
        
        
        temp_path.close()
        