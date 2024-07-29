import sqlite3
import datetime

def get_connection():
    return sqlite3.connect('blood_bank.db')

def add_donor(name, age, blood_group, department, contact_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO donors (name, age, blood_group, department, contact_number, status, last_donation_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, blood_group, department, contact_number, 'Ready to Donate', None))
    conn.commit()
    conn.close()

def get_donors_by_blood_group(blood_group):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM donors WHERE blood_group = ?', (blood_group,))
    donors = cursor.fetchall()
    conn.close()
    return donors

def update_donor_status(contact_number, department, status, last_donation_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE donors
    SET status = ?, last_donation_date = ?
    WHERE contact_number = ? AND department = ?
    ''', (status, last_donation_date, contact_number, department))
    conn.commit()
    conn.close()

def get_donor_by_contact_and_department(contact_number, department):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM donors WHERE contact_number = ? AND department = ?', (contact_number, department))
    donor = cursor.fetchone()
    conn.close()
    return donor

def check_and_update_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM donors')
    donors = cursor.fetchall()
    for donor in donors:
        if donor[6] == 'Donated' and donor[7] is not None:
            last_donation_date = datetime.datetime.strptime(donor[7], '%Y-%m-%d').date()
            if (datetime.date.today() - last_donation_date).days >= 90:
                cursor.execute('UPDATE donors SET status = ? WHERE id = ?', ('Ready to Donate', donor[0]))
    conn.commit()
    conn.close()
