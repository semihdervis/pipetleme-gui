import sqlite3
from dataclasses import dataclass
import hashlib
from datetime import datetime

# region Dataclasses
USER_TYPES = {0: "Üretici", 1: "Servis", 2: "Admin", 3: "User"}

@dataclass
class User:
    name: str
    password: str
    type: int


@dataclass
class Reagent:
    name: str
    ref_no: int
    barcode: int
    volume: int
    type: str
    check_date: int

@dataclass
class Settings:
    id: int = None
    system_name: str = ""
    serial_number: str = ""
    reader_port: str = ""
    reader_data_bit: int = 0
    reader_parity_bit: str = ""
    reader_baud_rate: int = 0
    reader_stop_bit: int = 0
    lis_port: str = ""
    lis_data_bit: int = 0
    lis_parity_bit: str = ""
    lis_baud_rate: int = 0
    lis_stop_bit: int = 0


@dataclass
class Layout:
    rack_name: str = ""
    rack_id: int = 0
    x_pos: int = 0
    y_pos: int = 0
    width: int = 0 
    height: int = 0
    row_count: int = 0
    column_count: int = 0
    hole_area: int = 0
    first_hole_x: int = 0
    first_hole_y: int = 0
    first_hole_z: int = 0
    last_hole_x: int = 0
    last_hole_y: int = 0
    last_hole_z: int = 0
    z_travel: int = 0
    z_scan: int = 0
    z_disp: int = 0
    z_max: int = 0
    description: str = ""


@dataclass
class Liquid:
    id: int 
    name: str
    trans_air_gap: int
    tip_air_gap: int
    aspirate_speed: int
    aspirate_ramp: int
    aspirate_delay: int
    detect_speed: int
    detect_ramp: int
    submerge: int
    additional_volume: int
    mix_speed: int
    mix_ramp: int
    track_speed: int
    track_ramp: int
    dispense_speed: int
    dispense_ramp: int
    dispense_delay: int
    enable_clot: int
    need_track: int
    detect_mode: int
    flush_tip_time: int


@dataclass
class Card:
    barcode: int
    card_name : str
    ref_no: int
    test_name: str
    card_type: str
    cell_define: str
    test_count: int
    is_used: int
    card_picture: str
    need_incubator: int
    incubation_time: int
    need_erythroracyte: int
    sample_volume: int
    sample_liquid: str
    liss_volume: int
    liss_liquid: str
    liss_reagent: str
    mix_volume: int
    mix_cycle: int
    mix_liquid: str
    asp_volume: int
    cell_sequence: str
    need_serum: int
    serum_volume: int
    serum_liquid: str
    serum_cell_sequence: str
    script: str


@dataclass
class Log:
    id: int
    time : datetime
    action: str
    user_name: str
    user_type: int
    details: str


# endregion


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("./yeni_gui/database.db")
        self.cursor = self.conn.cursor()


    # region User
    def check_user(self, username: str, password: str):
        password_hashed = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password_hashed))
        user = self.cursor.fetchone()

        if user:
            return User(*user)
        
        
    def add_user(self, user : User):
        password_hashed = hashlib.sha256(user.password.encode()).hexdigest()
        self.cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (?, ?, ?)", (user.name, password_hashed, user.type))
        self.conn.commit()
        return True
    
    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return [User(*user) for user in self.cursor.fetchall()]
    

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            return User(*user)
        else:
            return None
    

    def get_users_less_types(self, type):
        self.cursor.execute("SELECT * FROM users WHERE user_type >= ?", (type,))
        return [User(*user) for user in self.cursor.fetchall()]


    def update_user(self, old : User, new : User):
        self.cursor.execute("UPDATE Users SET username = ?, user_type = ? WHERE username = ?", (new.name, new.type, old.name))
        self.conn.commit()

    
    def delete_user(self, user : User):
        self.cursor.execute("DELETE FROM Users WHERE username = ?", (user.name,))
        self.conn.commit()

    def get_user_names(self):
        self.cursor.execute("SELECT username FROM Users")
        return [user[0] for user in self.cursor.fetchall()]

    # endregion


    # region Reagent

    def add_reagent(self, reagent : Reagent):
        self.cursor.execute("INSERT INTO Reagent (reagent_name, referance_no, barcode, volume, type, check_date) VALUES (?, ?, ?, ?, ?, ?)", (reagent.name, reagent.ref_no, reagent.barcode, reagent.volume, reagent.type, reagent.check_date))
        self.conn.commit()

    def get_reagents(self):
        self.cursor.execute("SELECT reagent_name, referance_no, barcode, volume, type, check_date FROM Reagent ORDER BY barcode")
        return [Reagent(*reagent) for reagent in self.cursor.fetchall()]

    def get_reagent_names(self):
        self.cursor.execute("SELECT reagent_name FROM Reagent")
        return [reagent[0] for reagent in self.cursor.fetchall()]

    def get_reagents_barcode(self):
        self.cursor.execute("SELECT barcode FROM Reagent")
        return [reagent[0] for reagent in self.cursor.fetchall()]
    
    def get_reagent(self, barcode):
        self.cursor.execute("SELECT reagent_name, referance_no, barcode, volume, type, check_date FROM Reagent WHERE barcode = ?", (barcode,))
        reagent = self.cursor.fetchone()
        if reagent:
            return Reagent(*reagent)
        else:
            return None
        
    def update_reagent(self, old : Reagent, new : Reagent):
        self.cursor.execute("UPDATE Reagent SET reagent_name = ?, referance_no = ?, barcode = ?, volume = ?, type = ?, check_date = ? WHERE barcode = ?", (new.name, new.ref_no, new.barcode, new.volume, new.type, new.check_date, old.barcode))
        self.conn.commit()
    
    def delete_reagent(self, reagent : Reagent):
        self.cursor.execute("DELETE FROM Reagent WHERE reagent_name = ? and barcode = ?", (reagent.name, reagent.barcode,))
        self.conn.commit()

    def delete_all_reagents(self):
        self.cursor.execute("DELETE FROM Reagent")
        self.conn.commit()

    def add_all_reagents(self, reagents):
        for reagent in reagents:
            self.add_reagent(reagent)

    # endregion


    # region Settings

    def get_settings(self):
        self.cursor.execute("SELECT * FROM Settings")
        settings = self.cursor.fetchone()
        if settings:
            return Settings(*settings)
        else:
            return None
        
    def delete_settings(self):
        self.cursor.execute("DELETE FROM Settings")
        self.conn.commit()

    def update_settings(self, settings : Settings):
        #update settings where id = 1
        self.cursor.execute("""UPDATE Settings SET system_name = ?, serial_number = ?, reader_port = ?, reader_data_bit = ?, reader_parity_bit = ?, reader_baud_rate = ?, reader_stop_bit = ?, lis_port = ?, lis_data_bit = ?, lis_parity_bit = ?, lis_baud_rate = ?, lis_stop_bit = ? WHERE id = 1""",
                            (settings.system_name, settings.serial_number, settings.reader_port, settings.reader_data_bit, settings.reader_parity_bit, settings.reader_baud_rate, settings.reader_stop_bit, settings.lis_port, settings.lis_data_bit, settings.lis_parity_bit, settings.lis_baud_rate, settings.lis_stop_bit))
        self.conn.commit()

    # endregion


    # region Liquid

    def get_liquid_names(self):
        self.cursor.execute("SELECT LiquidName FROM Liquid")
        return [liquid[0] for liquid in self.cursor.fetchall()]
    
    def get_liquid(self, name):
        self.cursor.execute("SELECT * FROM Liquid WHERE LiquidName = ?", (name,))
        liquid = self.cursor.fetchone()
        #ilk sütün alınmayacak devamı alınacak
        if liquid:
            return Liquid(*liquid)
        else:
            return None

    def insert_liquid(self, liquid : Liquid):
        self.cursor.execute("INSERT INTO Liquid (ID,LiquidName, TransAir, TipAir, AspSpd, AspRamp, AspDelay, DetectSpd, DetectRamp, Submerge, WasteVol, MixSpd, MixRamp, TrackSpd, TrackRamp, DispSpd, DispRamp, DispDelay, EnableClot, NeedTrack, DetectMode, FlushTipTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (liquid.id, liquid.name, liquid.trans_air_gap, liquid.tip_air_gap, liquid.aspirate_speed, liquid.aspirate_ramp, liquid.aspirate_delay, liquid.detect_speed, liquid.detect_ramp, liquid.submerge, liquid.additional_volume, liquid.mix_speed, liquid.mix_ramp, liquid.track_speed, liquid.track_ramp, liquid.dispense_speed, liquid.dispense_ramp, liquid.dispense_delay, liquid.enable_clot, liquid.need_track, liquid.detect_mode, liquid.flush_tip_time))
        self.conn.commit()
        
    def delete_liquid(self, name):
        self.cursor.execute("DELETE FROM Liquid WHERE LiquidName = ?", (name,))
        self.conn.commit()
    
    def update_liquid(self, liquid : Liquid):
        #update with name
        self.cursor.execute("""UPDATE Liquid SET TransAir = ?, TipAir = ?, AspSpd = ?, AspRamp = ?, AspDelay = ?, DetectSpd = ?, DetectRamp = ?, Submerge = ?, WasteVol = ?, MixSpd = ?, MixRamp = ?, TrackSpd = ?, TrackRamp = ?, DispSpd = ?, DispRamp = ?, DispDelay = ?, EnableClot = ?, NeedTrack = ?, DetectMode = ?, FlushTipTime = ? WHERE LiquidName = ?""",
                            (liquid.trans_air_gap, liquid.tip_air_gap, liquid.aspirate_speed, liquid.aspirate_ramp, liquid.aspirate_delay, liquid.detect_speed, liquid.detect_ramp, liquid.submerge, liquid.additional_volume, liquid.mix_speed, liquid.mix_ramp, liquid.track_speed, liquid.track_ramp, liquid.dispense_speed, liquid.dispense_ramp, liquid.dispense_delay, liquid.enable_clot, liquid.need_track, liquid.detect_mode, liquid.flush_tip_time, liquid.name))
        self.conn.commit()

    def liquid_max_id(self):
        self.cursor.execute("SELECT MAX(ID) FROM Liquid")
        return self.cursor.fetchone()[0]

    # endregion


    # region Layout

    def get_layout(self, rack_name, rack_id):
        self.cursor.execute("SELECT * FROM Layout WHERE rack_name = ? AND rack_id = ?", (rack_name, rack_id))
        layout = self.cursor.fetchone()
        if layout:
            return Layout(*layout)
        else:
            return None
        
    def update_layout(self, layout:Layout):
        self.cursor.execute("""UPDATE Layout SET x_pos = ?, y_pos = ?, width = ?, height = ?, row_count = ?, column_count = ?, hole_area = ?, first_hole_x = ?, first_hole_y = ?, first_hole_z = ?, last_hole_x = ?, last_hole_y = ?, last_hole_z = ?, z_travel = ?, z_scan = ?, z_disp = ?, z_max = ?, description = ? WHERE rack_name = ? AND rack_id = ?""",
                            (layout.x_pos, layout.y_pos, layout.width, layout.height, layout.row_count, layout.column_count, layout.hole_area, layout.first_hole_x, layout.first_hole_y, layout.first_hole_z, layout.last_hole_x, layout.last_hole_y, layout.last_hole_z, layout.z_travel, layout.z_scan, layout.z_disp, layout.z_max, layout.description, layout.rack_name, layout.rack_id))
        self.conn.commit()

    # endregion


    #region card

    def get_card_name(self, barcode):
        self.cursor.execute("SELECT card_name from Card where barcode = ?", (barcode,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_card_names(self):
        self.cursor.execute("SELECT card_name from Card")
        return [card[0] for card in self.cursor.fetchall()]
    

    def get_table_cards(self):
        #barcode,name,test-name
        #join with card and carddetail
        self.cursor.execute("""
        SELECT  
            C.barcode, C.card_name, CD.test_name
        FROM Card C
        INNER JOIN CardDetail CD ON C.barcode = CD.barcode
        """)
        
        return self.cursor.fetchall()

    
    def get_all_cards(self):
        self.cursor.execute("""
        SELECT 
            C.barcode, C.card_name, CD.ref_no, CD.test_name, CD.card_type, 
            CD.cell_define, CD.test_count, CD.is_used, CD.card_picture, 
            CD.need_incubator, CD.incubator_time, CD.need_erythrocyte, 
            CD.sample_volume, CD.sample_liquid, CD.liss_volume, CD.liss_liquid, 
            CD.liss_reagent, CD.mix_volume, CD.mix_cycle, CD.mix_liquid, 
            CD.asp_volume, CD.cell_sequence, CD.need_serum, CD.serum_volume, 
            CD.serum_liquid, CD.serum_cell_sequence, CD.script
        FROM Card C
        INNER JOIN CardDetail CD ON C.barcode = CD.barcode
        """)

        return [Card(*card) for card in self.cursor.fetchall()]
    
    def get_card(self, barcode,test_name):
        self.cursor.execute("""
        SELECT 
            C.barcode, C.card_name, CD.ref_no, CD.test_name, CD.card_type, 
            CD.cell_define, CD.test_count, CD.is_used, CD.card_picture, 
            CD.need_incubator, CD.incubator_time, CD.need_erythrocyte, 
            CD.sample_volume, CD.sample_liquid, CD.liss_volume, CD.liss_liquid, 
            CD.liss_reagent, CD.mix_volume, CD.mix_cycle, CD.mix_liquid, 
            CD.asp_volume, CD.cell_sequence, CD.need_serum, CD.serum_volume, 
            CD.serum_liquid, CD.serum_cell_sequence, CD.script
        FROM Card C
        INNER JOIN CardDetail CD ON C.barcode = CD.barcode
        WHERE C.barcode = ? AND CD.test_name = ?
        """, (barcode, test_name))

        card = self.cursor.fetchone()
        if card:
            return Card(*card)
        else:
            return None
        
    def delete_card(self, card : Card):
        self.cursor.execute("DELETE FROM CardDetail WHERE barcode = ? and test_name = ?", (card.barcode, card.test_name,))
        self.conn.commit()
    

    def update_card(self, card : Card):
        self.cursor.execute("""UPDATE CardDetail SET ref_no = ?, card_type = ?, cell_define = ?, test_count = ?, is_used = ?, card_picture = ?, need_incubator = ?, incubator_time = ?, need_erythrocyte = ?, sample_volume = ?, sample_liquid = ?, liss_volume = ?, liss_liquid = ?, liss_reagent = ?, mix_volume = ?, mix_cycle = ?, mix_liquid = ?, asp_volume = ?, cell_sequence = ?, need_serum = ?, serum_volume = ?, serum_liquid = ?, serum_cell_sequence = ?, script = ? WHERE barcode = ? AND test_name = ?""",
                            (card.ref_no, card.card_type, card.cell_define, card.test_count, card.is_used, card.card_picture, card.need_incubator, card.incubation_time, card.need_erythroracyte, card.sample_volume, card.sample_liquid, card.liss_volume, card.liss_liquid, card.liss_reagent, card.mix_volume, card.mix_cycle, card.mix_liquid, card.asp_volume, card.cell_sequence, card.need_serum, card.serum_volume, card.serum_liquid, card.serum_cell_sequence, card.script, card.barcode, card.test_name))
        
    
    def add_card_name(self, barcode, card_name):
        self.cursor.execute("INSERT INTO Card (barcode, card_name) VALUES (?, ?)", (barcode, card_name))
        self.conn.commit()

    def add_card(self, card : Card):
        self.cursor.execute("INSERT INTO CardDetail (barcode, ref_no, test_name, card_type, cell_define, test_count, is_used, card_picture, need_incubator, incubator_time, need_erythrocyte, sample_volume, sample_liquid, liss_volume, liss_liquid, liss_reagent, mix_volume, mix_cycle, mix_liquid, asp_volume, cell_sequence, need_serum, serum_volume, serum_liquid, serum_cell_sequence, script) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (card.barcode, card.ref_no, card.test_name, card.card_type, card.cell_define, card.test_count, card.is_used, card.card_picture, card.need_incubator, card.incubation_time, card.need_erythroracyte, card.sample_volume, card.sample_liquid, card.liss_volume, card.liss_liquid, card.liss_reagent, card.mix_volume, card.mix_cycle, card.mix_liquid, card.asp_volume, card.cell_sequence, card.need_serum, card.serum_volume, card.serum_liquid, card.serum_cell_sequence, card.script))
        self.conn.commit()
    

    # endregion


    # region Log

    def insert_log(self, action, user_name, user_type, description):
        self.cursor.execute("INSERT INTO Log (action, user_name, user_type, details) VALUES (?, ?, ?, ?)", (action, user_name, user_type, description))
        self.conn.commit()

    def get_logs(self):
        self.cursor.execute("SELECT * FROM Log")
        logs = self.cursor.fetchall()
        return [Log(*log) for log in logs]
    
    def filter_logs(self, start_time, end_time, user_names=None, user_types=None, actions=None):
        query = "SELECT * FROM Log WHERE time BETWEEN ? AND ?"
        params = [start_time, end_time]

        if user_names is not None:
            query += " AND user_name IN ({})".format(','.join('?' for _ in user_names))
            params.extend(user_names)

        if user_types is not None:
            query += " AND user_type IN ({})".format(','.join('?' for _ in user_types))
            params.extend(user_types)

        if actions is not None:
            query += " AND action IN ({})".format(','.join('?' for _ in actions))
            params.extend(actions)

        self.cursor.execute(query, params)
        logs = self.cursor.fetchall()
        return [Log(*log) for log in logs]
    
    # endregion