from jinja2 import Environment, FileSystemLoader
import datetime
import subprocess

def generate_report(results):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.md.j2')
    output = template.render(
        scan_results=results,
        generated_at=datetime.datetime.now().isoformat()
    )

    with open("report.md", "w") as f:
        f.write(output)
    print("✅ Report written to report.md")

    try:
        subprocess.run(["pandoc", "report.md", "-o", "report.pdf"], check=True)
        print("📄 PDF report written to report.pdf")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to generate PDF report (pandoc not installed?)")
