import sqlite3

conn1 = sqlite3.connect("company1.db")

cursor1 = conn1.cursor()

# =====================================================
# Main Ticket Table
# =====================================================

cursor1.execute("""
CREATE TABLE IF NOT EXISTS ticket_table (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    category TEXT,
    sentiment TEXT,
    priority TEXT,
    description TEXT,
    next_action TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# Workflow Log Table
# =====================================================

cursor1.execute("""
CREATE TABLE IF NOT EXISTS workflow_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    status TEXT,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# Callback Table
# =====================================================

cursor1.execute("""
CREATE TABLE IF NOT EXISTS callback_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    customer_id INTEGER,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# Refund Table
# =====================================================

cursor1.execute("""
CREATE TABLE IF NOT EXISTS refund_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    customer_id INTEGER,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# Cancellation Table
# =====================================================

cursor1.execute("""
CREATE TABLE IF NOT EXISTS cancellation_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    customer_id INTEGER,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =====================================================
# Trigger - Ticket Created
# =====================================================

cursor1.execute("""
CREATE TRIGGER IF NOT EXISTS trg_ticket_created
AFTER INSERT ON ticket_table
BEGIN

    INSERT INTO workflow_log (
        ticket_id,
        status,
        message
    )
    VALUES (
        NEW.ticket_id,
        'CREATED',
        'Ticket created successfully'
    );

END;
""")

# =====================================================
# Trigger - Callback Action
# =====================================================

cursor1.execute("""
CREATE TRIGGER IF NOT EXISTS trg_callback
AFTER INSERT ON ticket_table
WHEN UPPER(NEW.next_action) IN ('CALL BACK','CALLBACK')
BEGIN

    INSERT INTO callback_table (
        ticket_id,
        customer_id,
        description
    )
    VALUES (
        NEW.ticket_id,
        NEW.customer_id,
        NEW.description
    );

    INSERT INTO workflow_log (
        ticket_id,
        status,
        message
    )
    VALUES (
        NEW.ticket_id,
        'CALLBACK',
        'Callback Action initiated with database trigger'
    );

END;
""")

# =====================================================
# Trigger - Refund Action
# =====================================================

cursor1.execute("""
CREATE TRIGGER IF NOT EXISTS trg_refund
AFTER INSERT ON ticket_table
WHEN UPPER(NEW.next_action) = 'REFUND'
BEGIN

    INSERT INTO refund_table (
        ticket_id,
        customer_id,
        description
    )
    VALUES (
        NEW.ticket_id,
        NEW.customer_id,
        NEW.description
    );

    INSERT INTO workflow_log (
        ticket_id,
        status,
        message
    )
    VALUES (
        NEW.ticket_id,
        'REFUND',
        'Refund Action initiated with database trigger'
    );

END;
""")

# =====================================================
# Trigger - Cancellation Action
# =====================================================

cursor1.execute("""
CREATE TRIGGER IF NOT EXISTS trg_cancellation
AFTER INSERT ON ticket_table
WHEN UPPER(NEW.next_action) = 'CANCELLATION'
BEGIN

    INSERT INTO cancellation_table (
        ticket_id,
        customer_id,
        description
    )
    VALUES (
        NEW.ticket_id,
        NEW.customer_id,
        NEW.description
    );

    INSERT INTO workflow_log (
        ticket_id,
        status,
        message
    )
    VALUES (
        NEW.ticket_id,
        'CANCELLATION',
        'Cancellation Action initiated with database trigger'
    );

END;
""")

# =====================================================
# Start Ticket Number From 1000
# =====================================================

cursor1.execute("""
INSERT OR IGNORE INTO ticket_table (
    ticket_id,
    customer_id,
    category,
    sentiment,
    priority,
    description,
    next_action
)
VALUES (
    999,
    0,
    'INIT',
    'INIT',
    'LOW',
    'Initialization Record',
    'NONE'
)
""")

cursor1.execute("""
DELETE FROM ticket_table
WHERE ticket_id = 999
""")

conn1.commit()

conn1.close()

print("Database, tables and triggers created successfully.")