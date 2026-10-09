import asyncio
from scanner import VisionApp

async def main():
    """Main entry point for the scanner application."""
    app = VisionApp()
    
    print("=" * 60)
    print("MTG Card Scanner Tool")
    print("Open Source Multi-Mode Detection System")
    print("=" * 60)
    print(f"\nLoaded settings from: {app.config_path}")
    print(f"Settings: {app.settings if app.settings else 'Default (empty)'}")
    
    # Initialize database connection here when implemented
    
    print("\nMode selection:")
    print("1. Scan Mode - Capture multiple images, aggregate results")
    print("2. Tuning Mode - Debug view with parameter sliders")
    print("3. Auto-Tune Mode - Continuous detection and auto-adjustment")
    
    try:
        choice = input("\nSelect mode (1/2/3) or 's' for sample card list: ").lower().strip()
        
        if choice == 's':
            sample = app.load_sample_card_list()
            print(f"\nSample card list:\n{sample}")
            cards_input = input("Enter your test card names (or press Enter to use sample): ")
            if not cards_input:
                cards_input = sample
            
        elif choice == '1':
            cards_input = input("\nEnter card names to scan (comma or newline separated): ")
            test_cards = [c.strip() for c in cards_input.split(',') if c.strip()]
            
            if test_cards:
                print(f"\nScanning {len(test_cards)} cards...")
                for i, card_name in enumerate(test_cards, 1):
                    await app.capture_and_detect_one_image(card_name)
                
                accuracy = app.calculate_accuracy(test_cards)
                print(f"\nScan complete! Accuracy: {accuracy:.1f}%")
        
        elif choice == '2':
            app.show_tuning_mode()
        
        elif choice == '3':
            cards_input = input("\nEnter card names for auto-tune mode (comma or newline separated): ")
            test_cards = [c.strip() for c in cards_input.split(',') if c.strip()]
            
            if test_cards:
                results = await app.run_continuous_capture(test_cards)
                print(f"\nAuto-tune complete! Final accuracy: {results['final_accuracy']:.1f}%")
        
        else:
            print("\nInvalid mode selection. Showing scan interface by default.")
    
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
    
    # Always offer save settings option
    save_input = input("\nSave current settings? (y/n): ").lower().strip()
    if save_input == 'y':
        app.save_settings()

if __name__ == "__main__":
    asyncio.run(main())