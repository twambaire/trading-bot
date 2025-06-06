#!/usr/bin/env python3
"""
Script ya kusakinisha na kusanidi bot ya biashara
"""

import os
import sys
import subprocess
import getpass

def check_python_version():
    """Angalia toleo la Python"""
    if sys.version_info < (3, 7):
        print("⚠️ Tahadhari: Bot inahitaji Python 3.7 au zaidi.")
        return False
    return True

def install_requirements():
    """Sakinisha mahitaji"""
    print("📦 Kusakinisha mahitaji...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Mahitaji yamesakinishwa.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Imeshindwa kusakinisha mahitaji.")
        return False

def setup_env_file():
    """Tengeneza faili ya .env"""
    if os.path.exists(".env"):
        overwrite = input("Faili ya .env tayari ipo. Ungependa kuiandika upya? (n/y): ").lower() == 'y'
        if not overwrite:
            print("✅ Kutumia faili ya .env iliyopo.")
            return True
    
    print("\n📝 Kusanidi faili ya .env...")
    
    # MT5 credentials
    mt5_login = input("MT5 Login ID: ")
    mt5_password = getpass.getpass("MT5 Password: ")
    mt5_server = input("MT5 Server (mfano 'FBS-Demo'): ") or "FBS-Demo"
    
    # Myfxbook credentials
    use_myfxbook = input("Unataka kutumia Myfxbook kwa uchambuzi wa hisia? (y/n): ").lower() == 'y'
    if use_myfxbook:
        myfxbook_email = input("Myfxbook Email: ")
        myfxbook_password = getpass.getpass("Myfxbook Password: ")
    else:
        myfxbook_email = ""
        myfxbook_password = ""
    
    # Trading parameters
    symbols = input("Jozi za sarafu (zitenganishwe kwa koma, mfano 'EURUSD,GBPUSD'): ") or "EURUSD,GBPUSD,USDJPY,GBPJPY"
    risk_percent = input("Asilimia ya hatari (1.0 kwa default): ") or "1.0"
    max_spread_pips = input("Upana wa juu wa spread kwa pips (3.0 kwa default): ") or "3.0"
    min_sentiment = input("Kiwango cha chini cha hisia kwa ishara (60.0 kwa default): ") or "60.0"
    scan_interval = input("Muda wa kuangalia (sekunde) (60 kwa default): ") or "60"
    
    # Write to .env file
    with open(".env", "w") as f:
        f.write(f"""# MT5 Credentials
MT5_LOGIN={mt5_login}
MT5_PASSWORD={mt5_password}
MT5_SERVER={mt5_server}

# Myfxbook Credentials
MYFXBOOK_EMAIL={myfxbook_email}
MYFXBOOK_PASSWORD={myfxbook_password}

# Trading Parameters
SYMBOLS={symbols}
RISK_PERCENT={risk_percent}
MAX_SPREAD_PIPS={max_spread_pips}
MIN_SENTIMENT_THRESHOLD={min_sentiment}
SCAN_INTERVAL={scan_interval}
""")
    
    print("✅ Faili ya .env imetengenezwa.")
    return True

def main():
    """Mfumo mkuu wa kusakinisha"""
    print("🤖 Kusakinisha ICT Forex Trading Bot...")
    
    if not check_python_version():
        print("⚠️ Unaweza kupata matatizo kwa sababu ya toleo la Python.")
    
    if not install_requirements():
        print("❌ Imeshindwa kusakinisha. Tafadhali hakikisha una muunganisho wa intaneti na ujaribiu tena.")
        return
    
    if not setup_env_file():
        print("❌ Imeshindwa kusanidi faili ya .env.")
        return
    
    print("\n✅ Usakinishaji umekamilika!")
    print("\n🚀 Kuanza bot:")
    print("   python improved_scalper.py")

if __name__ == "__main__":
    main()

