import base64
import datetime
import json
import os
from pathlib import Path
from typing import Dict, List

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "company_name": "Your Company Name",
    "company_url": "https://example.com",
    "logo_path": "assets/default-logo.svg",
    "output_dir": "generated_invoices",
}

DEFAULT_CSS = """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    color: #333;
}
.invoice {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px;
    border: 1px solid #ddd;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
.invoice-header-wrapper {
    margin-bottom: 40px;
}
.invoice-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
.logo-section {
    flex: 0 0 200px;
}
.logo {
    max-width: 100%;
    height: auto;
}
.header-content {
    flex: 1;
    text-align: right;
}
h1 {
    margin: 0 0 20px;
    color: #2c3e50;
}
.client-info {
    margin-bottom: 20px;
}
.client-label {
    color: #666;
    font-size: 0.9em;
}
.org-name {
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 5px;
}
.tasks-list {
    margin-bottom: 40px;
}
.task-item {
    padding: 20px;
    background: #f9f9f9;
    margin-bottom: 10px;
    border-radius: 4px;
}
.task-details {
    margin-bottom: 15px;
}
.task-meta {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}
.label {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 5px;
}
.value {
    font-weight: bold;
}
.invoice-total {
    text-align: right;
    font-size: 1.2em;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 4px;
}
.invoice-footer {
    margin-top: 40px;
    text-align: center;
    color: #666;
    font-size: 0.9em;
}
.invoice-footer a {
    color: #3498db;
    text-decoration: none;
}
.invoice-footer a:hover {
    text-decoration: underline;
}
"""


def load_config() -> Dict:
    """Load configuration from config.json or create default if not exists"""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def setup_directories():
    """Create necessary directories if they don't exist"""
    Path("generated_invoices").mkdir(exist_ok=True)
    Path("assets").mkdir(exist_ok=True)


def get_invoice_info() -> Dict:
    print("\nInvoice Information")
    print("-" * 20)
    org_name = input("Enter client/organization name: ")
    while True:
        try:
            default_rate = float(input("Enter hourly rate (e.g., 50.00): $"))
            break
        except ValueError:
            print("Please enter a valid number")

    variable_rates = (
        input("Use variable rates for different tasks? (y/n): ").lower() == "y"
    )
    return {
        "org_name": org_name,
        "default_rate": default_rate,
        "variable_rates": variable_rates,
    }


def get_task_data(default_rate: float, variable_rates: bool) -> Dict:
    print("\nTask Information")
    print("-" * 16)
    task = input("Enter task description: ")

    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Please use the format YYYY-MM-DD")

    while True:
        try:
            hours = float(input("Enter hours spent: "))
            break
        except ValueError:
            print("Please enter a valid number")

    rate = default_rate
    if variable_rates:
        while True:
            try:
                rate = float(
                    input(f"Enter hourly rate (default: ${default_rate:.2f}): $")
                    or default_rate
                )
                break
            except ValueError:
                print("Please enter a valid number")

    return {
        "task": task,
        "date": date_str,
        "hours": hours,
        "rate": rate,
        "subtotal": hours * rate,
    }


def get_all_tasks(default_rate: float, variable_rates: bool) -> List[Dict]:
    tasks = []
    while True:
        tasks.append(get_task_data(default_rate, variable_rates))

        add_more = input("\nAdd another task? (y/n): ").lower()
        if add_more != "y":
            break
        print("\n--- Next Task ---")

    return tasks


def generate_tasks_html(tasks: List[Dict]) -> str:
    """Generate the HTML for tasks"""
    tasks_html = ""
    for task in tasks:
        tasks_html += f"""
            <div class="task-item">
                <div class="task-details">
                    <div class="label">Task Description</div>
                    <div class="value">{task['task']}</div>
                </div>
                <div class="task-meta">
                    <div>
                        <div class="label">Date</div>
                        <div class="value">{task['date']}</div>
                    </div>
                    <div>
                        <div class="label">Hours</div>
                        <div class="value">{task['hours']}</div>
                    </div>
                    <div>
                        <div class="label">Rate</div>
                        <div class="value">${task['rate']:.2f}/hr</div>
                    </div>
                    <div>
                        <div class="label">Subtotal</div>
                        <div class="value">${task['subtotal']:.2f}</div>
                    </div>
                </div>
            </div>
        """
    return tasks_html


def read_css_file() -> str:
    """Read the CSS file and return its contents"""
    try:
        with open("style.css", "r") as file:
            return file.read()
    except FileNotFoundError:
        return DEFAULT_CSS


def get_base64_logo(config: Dict) -> str:
    """Convert the logo SVG to base64"""
    import base64

    # Try to use configured logo path
    logo_path = config.get("logo_path", "src/assets/default-logo.svg")

    try:
        with open(logo_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
    except FileNotFoundError:
        # Fallback to default logo if custom logo not found
        try:
            with open("src/assets/default-logo.svg", "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        except FileNotFoundError:
            # If even default logo is missing, return a simple data URI
            return """
            PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjYwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPg
            0KICAgIDxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9Im5vbmUiLz4NCiAgICA8dGV4dCB4
            PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBmaWxsPSIjNjY2IiB0ZX
            h0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0ibWlkZGxlIj4NCiAgICAgICAgWW91ciBMb2dv
            IEhlcmUNCiAgICA8L3RleHQ+DQo8L3N2Zz4=
            """.strip()


def generate_invoice(org_name: str, tasks: List[Dict], config: Dict) -> str:
    """Generate the invoice and return the output filename"""
    # Generate filename
    output_dir = config.get("output_dir", "generated_invoices")
    filename = os.path.join(
        output_dir, f"{org_name.lower().replace(' ', '_')}-invoice.html"
    )
    total = sum(task["subtotal"] for task in tasks)

    # Read the CSS
    try:
        css = read_css_file()
    except FileNotFoundError:
        css = DEFAULT_CSS  # We'll define this constant at the top of the file

    # Create self-contained HTML with inlined CSS and print styles
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invoice - {org_name}</title>
        <style>
            {css}
            @media print {{
                body {{
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }}
                .invoice {{
                    border: none;
                    box-shadow: none;
                    margin: 0;
                    padding: 20px;
                }}
                .invoice-footer {{
                    position: fixed;
                    bottom: 20px;
                    left: 0;
                    right: 0;
                }}
                @page {{
                    margin: 0.5cm;
                    size: A4;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="invoice">
            <div class="invoice-header-wrapper">
                <div class="invoice-header">
                    <div class="logo-section">
                        <img src="data:image/svg+xml;base64,{get_base64_logo(config)}" alt="Logo" class="logo">
                    </div>
                    <div class="header-content">
                        <h1>Invoice</h1>
                        <div class="client-info">
                            <span class="client-label">Client</span>
                            <div class="org-name">{org_name}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="tasks-list">
                {generate_tasks_html(tasks)}
            </div>
            
            <div class="invoice-total">
                <div class="label">Total Amount</div>
                <div class="value">${total:.2f}</div>
            </div>

            <div class="invoice-footer">
                Billed by <a href="{config.get('company_url', '#')}">{config.get('company_name', 'Your Company Name')}</a>
            </div>
        </div>
    </body>
    </html>
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the file
    with open(filename, "w") as file:
        file.write(html_template)

    return filename


def main():
    print("Invoice Generator")
    print("=" * 16)

    setup_directories()
    config = load_config()

    invoice_info = get_invoice_info()
    tasks = get_all_tasks(invoice_info["default_rate"], invoice_info["variable_rates"])

    output_file = generate_invoice(invoice_info["org_name"], tasks, config)
    print(f"\nSuccess! Invoice generated at: {output_file}")
    print("\nTo create a PDF:")
    print("1. Open the HTML file in your web browser")
    print("2. Press Ctrl+P (Cmd+P on Mac)")
    print("3. Select 'Save as PDF' as the destination")
    print("4. Click 'Save'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

