def set_column_widths(table, widths):
    for i, width in enumerate(widths):
        table.setColumnWidth(i, width)

def create_primary_table(self):
    widths = [100, 197, 197, 197, 197, 197, 120]
    set_column_widths(self.table_memory_principal, widths)

def create_secondary_table(self):
    widths = [100, 197, 197, 197, 197, 197, 120]
    set_column_widths(self.table_memory_secondary, widths)