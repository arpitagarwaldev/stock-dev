#!/usr/bin/env python3
"""
Setup script for Stock Trading Simulator
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def setup_backend():
    """Setup backend dependencies"""
    print("\n🔧 Setting up backend...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Check if virtual environment exists
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        print("Creating virtual environment...")
        run_command("python -m venv venv", cwd=backend_dir)
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/Linux/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    # Install dependencies
    print("Installing Python dependencies...")
    requirements_file = backend_dir / "requirements.txt"
    
    if requirements_file.exists():
        result = run_command(f"{pip_path} install -r requirements.txt", cwd=backend_dir)
        if result is not None:
            print("✓ Backend dependencies installed")
        else:
            print("❌ Failed to install backend dependencies")
            return False
    else:
        print("❌ requirements.txt not found")
        return False
    
    return True

def setup_database():
    """Initialize the database"""
    print("\n🗄️  Setting up database...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Import and initialize database
    sys.path.append(str(backend_dir / "src"))
    
    try:
        from models.database import Database
        db = Database()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n📝 Setting up environment configuration...")
    
    backend_dir = Path(__file__).parent / "backend"
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        env_content = """FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
INITIAL_BALANCE=100000
DATABASE_PATH=trading.db
ALPHA_VANTAGE_API_KEY=demo
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✓ Environment file created")
    else:
        print("✓ Environment file already exists")

def print_instructions():
    """Print setup completion instructions"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python src/app.py")
    print("\n2. Open the frontend:")
    print("   Open frontend/index.html in your web browser")
    print("   Or serve it using a local server:")
    print("   cd frontend")
    print("   python -m http.server 8000")
    print("   Then visit: http://localhost:8000")
    print("\n3. Create an account and start trading!")
    print("\n💡 Tips:")
    print("- You start with $100,000 virtual money")
    print("- Stock prices are real-time from Yahoo Finance")
    print("- Try searching for popular stocks like AAPL, GOOGL, MSFT")
    print("- Use the watchlist to track stocks you're interested in")

def main():
    """Main setup function"""
    print("🚀 Stock Trading Simulator Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed")
        sys.exit(1)
    
    # Print instructions
    print_instructions()

if __name__ == "__main__":
    main()