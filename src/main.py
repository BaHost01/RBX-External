import requests

class OffsetManager:
    def __init__(self, rbx_version: str):
        self.rbx_version = rbx_version
        self.endpoint_url = f"https://offsets.imtheo.lol/{rbx_version}/offsetshex.json"
        self.raw_offsets = {}
        self.parsed_offsets = {}

    def fetch() -> bool:
        """Fetches raw JSON from the endpoint and triggers offset parsing."""
        try:
            response = requests.get(self.endpoint_url, timeout=10)
            if response.status_code == 200:
                self.raw_offsets = response.json()
                self._process_offsets()
                return True
            print(f"Failed to fetch offsets. HTTP status: {response.status_code}")
        except requests.RequestException as error:
            print(f"Network error fetching offsets: {error}")
        return False

    def _process_offsets(self):
        """Converts string hex representations into native integer addresses."""
        self.parsed_offsets.clear()
        for key, value in self.raw_offsets.items():
            if isinstance(value, str):
                try:
                    # Parse hex string (e.g., "0x1A2B" or "1A2B") to integer
                    self.parsed_offsets[key] = int(value, 16)
                except ValueError:
                    self.parsed_offsets[key] = value
            elif isinstance(value, int):
                self.parsed_offsets[key] = value
            else:
                self.parsed_offsets[key] = value

    def get_offset(self, name: str, default=None) -> int:
        """Retrieves an offset integer value by key name."""
        return self.parsed_offsets.get(name, default)

    def get_formatted_hex(self, name: str) -> str:
        """Returns the processed integer formatted back as a hex string."""
        val = self.get_offset(name)
        if isinstance(val, int):
            return f"0x{val:X}"
        return "N/A"

    def list_keys(self) -> list:
        """Returns all available offset keys."""
        return list(self.parsed_offsets.keys())


# Example integration into main workflow
def main():
    # Replace with detected active version folder
    rbx_version = "version-4310300497aa4917"
    
    manager = OffsetManager(rbx_version)
    if manager.fetch():
        print(f"Loaded {len(manager.parsed_offsets)} offsets.")
        
        # Example retrieval usage
        for key in manager.list_keys()[:5]:  # Display first 5 keys
            int_val = manager.get_offset(key)
            hex_val = manager.get_formatted_hex(key)
            print(f"Key: {key:<20} | Int: {int_val:<12} | Hex: {hex_val}")

if __name__ == "__main__":
    main()
