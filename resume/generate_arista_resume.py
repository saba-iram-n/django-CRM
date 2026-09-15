#!/usr/bin/env python3
"""Generate an ATS-friendly resume PDF tailored for Arista Networks SWE Intern."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

OUTPUT = "/workspace/resume/Surya_Shreevathsa_Arista_SWE_Intern.pdf"
ARTIFACT = "/opt/cursor/artifacts/Surya_Shreevathsa_Arista_SWE_Intern.pdf"

PAGE_W, PAGE_H = letter
LEFT = 0.6 * inch
RIGHT = PAGE_W - 0.6 * inch
TOP = PAGE_H - 0.45 * inch
BOTTOM = 0.45 * inch
CONTENT_W = RIGHT - LEFT

INK = HexColor("#111111")
MUTED = HexColor("#333333")
RULE = HexColor("#222222")

# Prefer system fonts that look professional and parse cleanly for ATS
FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def draw_hr(c, y):
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(LEFT, y, RIGHT, y)
    return y - 8


def section_header(c, title, y):
    c.setFont(FONT_BOLD, 10.5)
    c.setFillColor(INK)
    c.drawString(LEFT, y, title.upper())
    y -= 3
    y = draw_hr(c, y)
    return y


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        trial = w if not current else current + " " + w
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c, text, x, y, font, size, max_width, leading, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    lines = wrap_text(text, font, size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def bullet(c, text, y, indent=10, bullet_gap=8):
    """Draw a simple hyphen bullet for ATS readability."""
    max_w = CONTENT_W - indent - bullet_gap
    lines = wrap_text(text, FONT_REG, 9, max_w)
    c.setFillColor(INK)
    c.setFont(FONT_REG, 9)
    c.drawString(LEFT + indent, y, "-")
    x = LEFT + indent + bullet_gap
    for i, line in enumerate(lines):
        c.drawString(x, y, line)
        y -= 11.5
    return y - 1.5


def job_header(c, title, dates, y):
    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(INK)
    c.drawString(LEFT, y, title)
    c.setFont(FONT_REG, 9)
    c.setFillColor(MUTED)
    tw = pdfmetrics.stringWidth(dates, FONT_REG, 9)
    c.drawRightString(RIGHT, y, dates)
    return y - 12


def build():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("Surya Shreevathsa K. S - Resume")
    c.setAuthor("Surya Shreevathsa K. S")
    y = TOP

    # Name
    c.setFont(FONT_BOLD, 16)
    c.setFillColor(INK)
    name = "Surya Shreevathsa K. S"
    c.drawCentredString(PAGE_W / 2, y, name)
    y -= 14

    # Contact line (plain text; ATS friendly)
    contact = (
        "Mysuru, Karnataka  |  suryashreevathsa11@gmail.com  |  +91 8762110297  |  "
        "linkedin.com/in/surya-shreevathsa  |  github.com/surya-shreevathsa11"
    )
    c.setFont(FONT_REG, 8)
    c.setFillColor(MUTED)
    # center-wrap if needed
    if pdfmetrics.stringWidth(contact, FONT_REG, 8) > CONTENT_W:
        y = draw_wrapped(c, contact, LEFT, y, FONT_REG, 8, CONTENT_W, 10, MUTED)
        # re-center manually is hard after wrap; left align is fine for ATS
    else:
        c.drawCentredString(PAGE_W / 2, y, contact)
        y -= 12

    # Clickable links
    c.linkURL(
        "mailto:suryashreevathsa11@gmail.com",
        (LEFT, y + 2, RIGHT, y + 22),
        relative=0,
    )
    c.linkURL(
        "https://www.linkedin.com/in/surya-shreevathsa",
        (LEFT, y + 2, RIGHT, y + 22),
        relative=0,
    )
    c.linkURL(
        "https://github.com/surya-shreevathsa11",
        (LEFT, y + 2, RIGHT, y + 22),
        relative=0,
    )

    y -= 2
    y = draw_hr(c, y)
    y -= 2

    # SUMMARY
    y = section_header(c, "Summary", y)
    summary = (
        "Graduate engineer with hands-on C/C++ firmware, Linux, and embedded hardware "
        "interface work. Experience writing firmware over UART, I2C, SPI, and CAN, "
        "designing PCBs, and building telemetry pipelines on Linux. Comfortable working "
        "at the software and hardware boundary, from PCB design through firmware and "
        "data collection."
    )
    y = draw_wrapped(c, summary, LEFT, y, FONT_REG, 9, CONTENT_W, 11.5)
    y -= 6

    # SKILLS (only real skills; ordered toward Arista keywords they actually have)
    y = section_header(c, "Skills", y)
    skills = [
        (
            "Programming:",
            "C, C++, Python, Embedded C",
        ),
        (
            "Systems & Tools:",
            "Linux, Unix commands, Git, GitHub, FreeRTOS",
        ),
        (
            "Embedded & Buses:",
            "UART, I2C, SPI, CAN, Firmware development, Raspberry Pi, ESP32, Teensy",
        ),
        (
            "Electronics:",
            "PCB design (KiCad), Circuit design, Digital electronics, Battery management systems",
        ),
        (
            "Web (secondary):",
            "React, Node.js, Express, MongoDB, Tailwind CSS",
        ),
        (
            "Languages:",
            "English, Kannada, Hindi",
        ),
    ]
    for label, value in skills:
        c.setFont(FONT_BOLD, 9)
        c.setFillColor(INK)
        c.drawString(LEFT, y, label)
        label_w = pdfmetrics.stringWidth(label + " ", FONT_BOLD, 9)
        y = draw_wrapped(
            c, value, LEFT + label_w, y, FONT_REG, 9, CONTENT_W - label_w, 11.5
        )
        y -= 1
    y -= 4

    # EXPERIENCE
    y = section_header(c, "Work Experience", y)

    y = job_header(
        c,
        "Embedded Systems Engineer - Meen Motors (Bengaluru)",
        "Oct 2025 - Present",
        y,
    )
    c.setFont(FONT_REG, 8.5)
    c.setFillColor(MUTED)
    c.drawString(LEFT, y, "Previously Embedded Systems Intern, Jun 2025 - Oct 2025")
    y -= 12

    bullets_meen = [
        "Designed the electrical powertrain for a retro EV prototype: battery pack, DC-DC converters, relay switching, VESC motor controller, and wiring laid out for safety and thermal limits.",
        "Designed and fabricated the vehicle ECU PCB in KiCad (Teensy 4.1, MOSFET gate drivers, level shifting, harness connectors), plus steering-wheel HMI boards and battery sensing and charging circuits.",
        "Wrote Teensy 4.1 ECU firmware in C++ for vehicle access control, lighting, propulsion enable, BLE owner presence, battery state indication, and USB telemetry to in-car systems.",
        "Built an onboard telemetry pipeline on Raspberry Pi 5 (Linux) that collects live voltage, current, and battery health data and feeds a dashboard display.",
        "Integrated dual-lav mic path on the ECU board with analog switching into a phone TRRS jack; firmware selects mics from BLE proximity and the vehicle start button.",
    ]
    for b in bullets_meen:
        y = bullet(c, b, y)
    y -= 4

    y = job_header(
        c,
        "Freelance Software Engineer - Vara",
        "Jan 2026 - Present",
        y,
    )
    bullets_vara = [
        "Build and maintain web products for hospitality clients, including a live SaaS booking platform used by multiple properties.",
        "Ship responsive sites with Tailwind CSS; built Vara Labs (React, Node.js, Express, MongoDB) with Razorpay payments, currently live with 5 properties.",
    ]
    for b in bullets_vara:
        y = bullet(c, b, y)
    y -= 4

    y = job_header(
        c,
        "Intern - Hindustan Aeronautics Limited (HAL)",
        "Oct 2023 - Nov 2023",
        y,
    )
    y = bullet(
        c,
        "Observed LRU testing workflows and cockpit avionics systems; gained exposure to safety-critical hardware validation processes and SOPs in a defence manufacturing environment.",
        y,
    )
    y -= 4

    # EDUCATION
    y = section_header(c, "Education", y)
    y = job_header(
        c,
        "B.E. (EEE) - The National Institute of Engineering, Mysuru",
        "2021 - 2025",
        y,
    )
    y = job_header(
        c,
        "Class XII - Jawahar Navodaya Vidyalaya, Kodagu",
        "2020 - 2021",
        y,
    )
    y -= 4

    # PROJECTS (embedded-heavy for Arista fit)
    y = section_header(c, "Projects", y)

    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(INK)
    c.drawString(LEFT, y, "Design of Electric Go-Kart")
    c.setFont(FONT_REG, 9)
    c.setFillColor(MUTED)
    c.drawRightString(RIGHT, y, "2025")
    y -= 12
    for b in [
        "Designed a custom 17s13p lithium-ion battery pack and the high and low voltage architecture, with a safety interlock so the high voltage tractive system can only energise after the low voltage system is live (Accumulator Isolation Relay).",
        "Integrated safety systems including TSAL, RDS, and AIR-controlled tractive disconnect; validated performance targets in OptimumLap before the prototype was built and driven.",
    ]:
        y = bullet(c, b, y)
    y -= 3

    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(INK)
    c.drawString(LEFT, y, "Accident Alert System using Arduino")
    c.setFont(FONT_REG, 9)
    c.setFillColor(MUTED)
    c.drawRightString(RIGHT, y, "2024")
    y -= 12
    y = bullet(
        c,
        "Built crash detection with dual-trigger logic (MPU6050 impact plus GPS speed drop to zero) to cut false positives; on confirm, auto-sends an SMS with GPS coordinates to emergency contacts.",
        y,
    )
    y -= 3

    c.setFont(FONT_BOLD, 9.5)
    c.setFillColor(INK)
    c.drawString(LEFT, y, "Vara Labs")
    c.setFont(FONT_REG, 9)
    c.setFillColor(MUTED)
    c.drawRightString(RIGHT, y, "2026")
    # link annotation for project
    title_w = pdfmetrics.stringWidth("Vara Labs", FONT_BOLD, 9.5)
    c.linkURL(
        "https://www.varalabs.in/",
        (LEFT, y, LEFT + title_w, y + 10),
        relative=0,
    )
    y -= 12
    y = bullet(
        c,
        "Full-stack SaaS for property owners (React, Node.js, Express, MongoDB): bookings, pricing, availability, Google OAuth, and Razorpay with webhook verification.",
        y,
    )
    y -= 4

    # CERTIFICATIONS (most relevant only)
    y = section_header(c, "Certifications", y)
    certs = [
        ("Embedded Systems Certification Course: Embedded C, 8051, Arduino and Simulation - ASDC (DIY Guru)", "2026"),
        ("Electric Vehicle Essentials 2: Motors, Electrification and Charging System - ASDC (DIY Guru)", "2025"),
        ("Electric Vehicle Essentials 1: Industry Ecosystem and Battery Technology - ASDC (DIY Guru)", "2025"),
        ("Electronics and Circuit Design for EV Application - ASDC (DIY Guru)", "2025"),
        ("Introduction to the Internet of Things and Embedded System - University of California, Irvine (Coursera)", "2024"),
        ("Sensor and Sensor Circuit - University of Colorado Boulder (Coursera)", "2023"),
    ]
    for text, year in certs:
        c.setFont(FONT_REG, 8.5)
        c.setFillColor(INK)
        max_w = CONTENT_W - 40
        lines = wrap_text(text, FONT_REG, 8.5, max_w)
        c.drawRightString(RIGHT, y, year)
        for i, line in enumerate(lines):
            c.drawString(LEFT, y, line)
            y -= 10.5
        y -= 0.5

    c.save()

    # also copy to artifacts
    import shutil

    shutil.copy2(OUTPUT, ARTIFACT)
    print(f"Wrote {OUTPUT}")
    print(f"Copied {ARTIFACT}")


if __name__ == "__main__":
    build()
