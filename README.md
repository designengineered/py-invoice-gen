# Invoice Generator CLI

A simple command-line tool to generate professional HTML invoices that can be easily converted to PDF.

## Features

- Interactive CLI interface for entering invoice details
- Support for multiple tasks per invoice
- Configurable company details and branding
- Custom hourly rates (fixed or variable per task)
- Professional HTML output with print-optimized styling
- Easy conversion to PDF using browser print function

## Setup

1. Ensure you have Python installed on your system
2. Clone this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create necessary directories (will be created automatically on first run):
   - `assets/` - for storing logo files
   - `invoices/` - for generated invoice files

## Configuration

The tool uses a `config.json` file for basic settings. You can create or modify it with the following structure:

```json
{
    "company": {
        "name": "Your Company Name",
        "address": "123 Main St, City, State, ZIP",
        "phone": "555-1234",
        "email": "info@yourcompany.com"
    },
    "tasks": [
        {
            "name": "Task 1",
            "rate": 50
        },
        {
            "name": "Task 2",
            "rate": 60
        }
    ]
}
```

### Configuration Options:
- `company`: Your business details
  - `name`: Company name that appears on invoices
  - `address`: Full company address
  - `phone`: Contact phone number
  - `email`: Contact email address
- `tasks`: Predefined list of tasks with default rates
  - `name`: Task name/description
  - `rate`: Default hourly rate for this task type

If no config file exists, the tool will create one with default values.

## Using the CLI

### Starting the Tool
```bash
python cli.py
```

### Interactive Prompts

1. **Client Information**
   ```
   Enter client/organization name: [Client Name]
   ```

2. **Task Selection**
   ```
   Select task type or enter custom task:
   1. Task 1 ($50/hr)
   2. Task 2 ($60/hr)
   3. Custom task
   ```

3. **Task Details**
   ```
   Enter task date (YYYY-MM-DD): [Date]
   Enter hours spent: [Hours]
   ```

4. **Adding More Tasks**
   ```
   Add another task? (y/n): [y/n]
   ```

### Example Session
```bash
$ python cli.py
Enter client/organization name: Acme Corp
Select task type:
1. Task 1 ($50/hr)
2. Task 2 ($60/hr)
3. Custom task
Choice: 1
Enter task date (YYYY-MM-DD): 2024-03-15
Enter hours spent: 8
Add another task? (y/n): n
```

### Output
The tool will generate an HTML invoice in the `generated-invoices` directory. The filename will include the client name and date.

## Converting to PDF

1. Open the generated HTML file in your browser
2. Press `Ctrl+P` (or `Cmd+P` on Mac)
3. Select "Save as PDF" in the print dialog
4. Click "Save"

## Tips

- Dates must be in YYYY-MM-DD format
- You can press Ctrl+C at any time to cancel invoice generation
- The generated HTML is optimized for A4 paper size
- All monetary values are in USD