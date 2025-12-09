"""
GPU-SIM: Virtual GPU Simulator for Windows
Main entry point for the application.
"""

import sys
import os
import ctypes
import argparse
import logging
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def is_admin() -> bool:
    """Check if running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def request_admin():
    """Request Administrator privileges by relaunching with UAC."""
    if os.name != 'nt':
        return False

    try:
        # Re-run the script with admin rights
        script = sys.argv[0]
        params = ' '.join(sys.argv[1:])

        # ShellExecuteW returns > 32 on success
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        return result > 32
    except Exception:
        return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="GPU-SIM: Virtual GPU Simulator for Windows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              Launch the GUI control panel
  python main.py --cli        Run in CLI mode (show WMI info)
  python main.py --debug      Enable debug logging
  python main.py --list       List available GPU profiles
        """
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode (no GUI)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available GPU profiles"
    )

    parser.add_argument(
        "--wmi",
        action="store_true",
        help="Show current WMI GPU information"
    )

    parser.add_argument(
        "--profile",
        type=str,
        help="Apply a GPU profile (requires --apply)"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the specified profile to registry"
    )

    return parser.parse_args()


def setup_logging(debug: bool = False):
    """Configure logging."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def run_cli(args):
    """Run in CLI mode."""
    from src.core.config_manager import get_config_manager

    config = get_config_manager()

    if args.list:
        print("\n" + "=" * 50)
        print("  Available GPU Profiles")
        print("=" * 50 + "\n")

        profiles = config.list_profiles()
        if not profiles:
            print("No profiles found!")
            return

        for profile in profiles:
            print(f"  [{profile.id}]")
            print(f"    Name: {profile.name}")
            print(f"    VRAM: {profile.vram_gb:.0f} GB | Driver: {profile.driver_version}")
            print()

    if args.wmi:
        try:
            from src.wmi.wmi_monitor import get_wmi_monitor
            monitor = get_wmi_monitor()
            monitor.print_gpu_summary()
        except Exception as e:
            print(f"Error querying WMI: {e}")

    if args.profile and args.apply:
        print(f"\n[*] Applying profile: {args.profile}")

        profile = config.get_profile(args.profile)
        if not profile:
            print(f"[ERROR] Profile not found: {args.profile}")
            return

        try:
            from src.registry.gpu_registry import get_gpu_registry
            registry = get_gpu_registry()

            success = registry.apply_gpu_profile(profile)
            if success:
                print("[SUCCESS] Profile applied! Restart required.")
            else:
                print("[ERROR] Failed to apply profile. Run as Administrator.")
        except Exception as e:
            print(f"[ERROR] {e}")


def run_gui():
    """Run the GUI application."""
    from src.ui.main_window import main
    main()


def main():
    """Main entry point."""
    args = parse_args()
    setup_logging(args.debug)

    print("""
    ╔═══════════════════════════════════════════╗
    ║           GPU-SIM Control Panel           ║
    ║      Virtual GPU Simulator for Windows    ║
    ╚═══════════════════════════════════════════╝
    """)

    if args.cli or args.list or args.wmi or (args.profile and args.apply):
        run_cli(args)
    else:
        # GUI mode - check for admin privileges
        if not is_admin():
            print("    ⚠️  Administrator privileges required for full functionality.")
            print("    🔄 Requesting elevation...")
            if request_admin():
                sys.exit(0)  # Exit this instance, elevated one will run
            else:
                print("    ⚠️  Running without admin - some features may not work.")

        run_gui()


if __name__ == "__main__":
    main()
