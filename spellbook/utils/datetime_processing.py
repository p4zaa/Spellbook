from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
import warnings

def parse_thai_date(date_str: str, return_date_only: bool = True):
    # Thai month abbreviations and full names
    thai_months = {
        "ม.ค.": 1, "มกราคม": 1,
        "ก.พ.": 2, "กุมภาพันธ์": 2,
        "มี.ค.": 3, "มีนาคม": 3,
        "เม.ย.": 4, "เมษายน": 4,
        "พ.ค.": 5, "พฤษภาคม": 5,
        "มิ.ย.": 6, "มิถุนายน": 6,
        "ก.ค.": 7, "กรกฎาคม": 7,
        "ส.ค.": 8, "สิงหาคม": 8,
        "ก.ย.": 9, "กันยายน": 9,
        "ต.ค.": 10, "ตุลาคม": 10,
        "พ.ย.": 11, "พฤศจิกายน": 11,
        "ธ.ค.": 12, "ธันวาคม": 12
    }

    date_str = date_str.strip()

    def finalize(dt: datetime):
        return dt.date() if return_date_only else dt

    now = datetime.now()

    try:
        # --- Case 1: keywords ---
        if date_str == "วันนี้":
            return finalize(now)
        if date_str == "เมื่อวาน":
            return finalize(now - timedelta(days=1))
        if date_str == "พรุ่งนี้":
            return finalize(now + timedelta(days=1))
        if date_str == "มะรืนนี้":
            return finalize(now + timedelta(days=2))

        # --- Case 2: relative past ---
        if match := re.match(r"(\d+)\s*วันที่ผ่านมา", date_str):
            return finalize(now - timedelta(days=int(match.group(1))))
        if match := re.match(r"(\d+)\s*ชั่วโมงที่ผ่านมา", date_str):
            return finalize(now - timedelta(hours=int(match.group(1))))
        if match := re.match(r"(\d+)\s*นาทีที่ผ่านมา", date_str):
            return finalize(now - timedelta(minutes=int(match.group(1))))
        if match := re.match(r"(\d+)\s*สัปดาห์ที่ผ่านมา", date_str):
            return finalize(now - timedelta(weeks=int(match.group(1))))
        if match := re.match(r"(\d+)\s*เดือนที่ผ่านมา", date_str):
            return finalize(now - relativedelta(months=int(match.group(1))))
        if match := re.match(r"(\d+)\s*ปีที่ผ่านมา", date_str):
            return finalize(now - relativedelta(years=int(match.group(1))))

        # --- Case 3: relative future ---
        if match := re.match(r"อีก\s*(\d+)\s*วัน", date_str):
            return finalize(now + timedelta(days=int(match.group(1))))
        if match := re.match(r"อีก\s*(\d+)\s*ชั่วโมง", date_str):
            return finalize(now + timedelta(hours=int(match.group(1))))
        if match := re.match(r"อีก\s*(\d+)\s*นาที", date_str):
            return finalize(now + timedelta(minutes=int(match.group(1))))
        if match := re.match(r"อีก\s*(\d+)\s*สัปดาห์", date_str):
            return finalize(now + timedelta(weeks=int(match.group(1))))
        if match := re.match(r"อีก\s*(\d+)\s*เดือน", date_str):
            return finalize(now + relativedelta(months=int(match.group(1))))
        if match := re.match(r"อีก\s*(\d+)\s*ปี", date_str):
            return finalize(now + relativedelta(years=int(match.group(1))))

        # --- Case 4: absolute dates ---
        parts = date_str.split()
        if len(parts) == 3:
            day = int(parts[0])
            month = thai_months.get(parts[1])
            if month is None:
                warnings.warn(f"Unrecognized month: {parts[1]}")
                return None
            year = int(parts[2])

            # Convert BE (พ.ศ.) to CE (ค.ศ.)
            if year > 2400:  # full Buddhist year
                year -= 543
            elif year < 100:  # short year
                year += 2500 - 543

            return finalize(datetime(year, month, day))

        # If none of the patterns matched
        warnings.warn(f"Unrecognized date format: {date_str}")
        return None

    except Exception as e:
        warnings.warn(f"Error parsing date '{date_str}': {e}")
        return None

# --- Examples ---
'''print(parse_thai_date("2 มกราคม 2568"))
print(parse_thai_date("2 ม.ค. 2568"))        # 2025-01-02
print(parse_thai_date("6 วันที่ผ่านมา"))      # now - 6 days
print(parse_thai_date("3 ชั่วโมงที่ผ่านมา"))  # now - 3h
print(parse_thai_date("15 นาทีที่ผ่านมา"))    # now - 15m
print(parse_thai_date("2 สัปดาห์ที่ผ่านมา")) # now - 2 weeks
print(parse_thai_date("1 เดือนที่ผ่านมา"))    # now - 1 month
print(parse_thai_date("3 ปีที่ผ่านมา"))       # now - 3 years

print(parse_thai_date("วันนี้"))              # today
print(parse_thai_date("เมื่อวาน"))            # yesterday
print(parse_thai_date("พรุ่งนี้"))            # tomorrow
print(parse_thai_date("มะรืนนี้"))            # day after tomorrow

print(parse_thai_date("อีก 3 วัน"))           # now + 3 days
print(parse_thai_date("อีก 2 ชั่วโมง"))       # now + 2h
print(parse_thai_date("อีก 10 นาที"))         # now + 10m
print(parse_thai_date("อีก 2 สัปดาห์"))      # now + 2 weeks
print(parse_thai_date("อีก 1 เดือน"))         # now + 1 month
print(parse_thai_date("อีก 3 ปี"))            # now + 3 years
print(parse_thai_date('อัยรัย'))'''