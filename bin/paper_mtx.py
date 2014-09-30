#! /usr/bin/python
#
# handle the tape changer
#
# dconover 20140922

from subprocess import check_output
import re, pymysql
from random import randint

class changer:
    'simple tape changer class'

    def __init__ (self,pid):
        self.pid = pid
        self._tape_dev='/dev/changer'
        self.check_inventory()
        self.tape_drives = drives()
        self.mtxdb = mtxdb()
        
    def check_inventory(self):
        output = check_output(['mtx','status']).decode("utf-8")
        lines  = output.split('\n')
        self.drive_ids, self.tape_slot = self.split_mtx_output(output)

    def tape_slot(self,tape_id):
        return self.tape_slot[tape_id]

    def load_tape_pair(self):
        """load the next available tape pair"""
        if self.drives_empty():
           ids = self.mtxdb.select_ids()
           if len(ids) == 2:
               for drive id in enumerate(ids):
                   self.load_tape(id,drive)

    def unload_tape_pair(self):
        'unload the tapes in the current drives'
        if not self.drives_empty():
            for tape_id in self.tape_slot:
                self.unload_tape(tape_id)
           
    def drives_empty(self):
        self.check_inventory()
        return not len(self.drive_ids)

    def drives_loaded(self):
        self.check_inventory()
        if len(self.drive_ids)
            return(self.get_drive_tape_ids())
        else:
            return False

    def get_drive_tape_ids(self):
        self.check_inventory()
        return self.drive_ids
        

    def load_tape (self, tape_id, tape_drive):
        """Load a tape into a free drive slot"""
        if self.tape_slot[tape_id]:
            output = check_output(['mtx','load', self.tape_slot[tape_id], tape_drive])
            self.check_inventory()

    def unload_tape (self, tape_id):
        if self.drive_ids[tape_id]:
            output = check_output(['mtx','unload',self.drive_ids(tape_id)])
            self.check_inventory()

    def write_tape(self, dir):
        """write data to tape"""
        ## tar dir to two drives
        pass 

    def unload_tape(self, tape_id):
        """Unload a tape from a drive and put in the original slot""" 
        if self.drive_slots[tape_id]:
            output = check_output(['mtx','unload', tape_slot[tape_id], tape_drive])
            self.check_inventory()

    def split_mtx_output(self,mtx_output):
        """Return dictionaries of tape_ids in drives and slots."""
        drive_ids = {}
        tape_slot = {}

        for line in mtx_output.split('\n'):
            drive_line =   re.compile('^Data Transfer Element (\d):Full \(Storage Element (\d+) Loaded\):VolumeTag = ([A-Z0-9]{8})')
            storage_line = re.compile('\s+Storage Element (\d+):Full :VolumeTag=([A-Z0-9]{8})')

            if drive_line.match(line):
                """Data Transfer Element 1:Full (Storage Element 1 Loaded):VolumeTag = PAPR1001"""
                drive_info = drive_line.match(line).groups()
                ## dict of storage_slots by tape_id
                drive_ids[drive_info[2]] = drive_info[0:2]

            elif storage_line.match(line):
                """Storage Element 10:Full :VolumeTag=PAPR1010"""
                storage_info = storage_line.match(line).groups()
                ## dict of tapes slots by tape_id
                tape_slot[storage_info[1]] = storage_info[0]

        return drive_ids, tape_slot

class mtxdb:
    """class to handle record of label ids

    Field     Type    Null    Key     Default Extra
    id        mediumint(9)    NO      PRI     NULL    auto_increment
    label     char(8) YES             NULL
    date      int(11) YES             NULL
    status    int(11) YES             NULL
    capacity  int(11) YES             NULL

    """

    def __init__ (self, _credentials, pid):
        """Initialize connection and collect list of tape_ids.""" 

        self.pid = pid
        self.connect = pymysql.connect(read_default_file=_credentials)
        self.cur = self.connect.cursor()

    def get_capacity(self, tape_id):
        select_sql = "select capacity from ids where id='%s'" % (tape_id)

    def select_ids(self):
        """select lowest matching id pairs"""

        ids = []
        for n in [0,1]:
            select_sql = "select label from ids where status is null and label like 'PAPR%d%s'" % (n+1,"%")
            self.cur.execute(select_sql)
            
            #print(self.cur.fetchone()[0])
            ids.append(self.cur.fetchone()[0])
        return ids

    def insert_ids(self, ids):
        """Add new tape_ids to the mtxdb"""
        for id in ids:
            insert_sql = "insert into ids (label) values('%s')" % id
            print(insert_sql)
            self.cur.execute(insert_sql)

        self.connect.commit()

    def claim_ids (self, ids):
        """Mark files in the database that are "claimed" by a dump process."""
        for id in ids:
            claim_query = 'update ids set status=%s where label=%s' % (self.pid,id)
            self.cur.execute(claim_query)

        self.connect.commit()

    def write(self, src_directory):
        """take a path like /dev/shm/1003261778 and create a tar archive on two tapes"""

        self.update_unused_capacity()
        pass

    def update_unused_capacity(self,used):
        """Write out unused capacity to database."""
        
        pass

    def __del__ (self):
        self.cur.close()
        self.connect.close()
            
                
class drives:
    """class to write two tapes"""

    def __init__(self):
        self.nst0 = '/dev/nst0'
        self.nst1 = '/dev/nst1'

    def write(self,text):
        self.nst0.write(text)
        self.nst0.write(text)

    def flush(self):
        self.nst0.flush(text)
        self.nst0.flush(text)

    def __del__(self):
        self.nst0.close()
        self.nst1.close()
