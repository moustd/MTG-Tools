from dataclasses import dataclass

@dataclass
class CardRecord:
    """Data class for database records."""
    id: int = 0
    name: str = ""
    scryfall_id: str = ""
    cost: str = ""
    type_line: str = ""
    rarity: str = ""
    power_toughness: str = "-"
    idhrec_rank: int = 0
    idhrec_inclusion_rate: float = 0.0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage/export."""
        return {
            "name": self.name,
            "scryfall_id": self.scryfall_id,
            "cost": self.cost,
            "type_line": self.type_line,
            "rarity": self.rarity,
            "power_toughness": self.power_toughness,
            "idhrec_rank": self.idhrec_rank,
            "idhrec_inclusion_rate": self.idhrec_inclusion_rate
        }