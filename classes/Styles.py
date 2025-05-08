
class Style:
  def __init__(self, style):
    self.style = style
    
    style.configure(
      "success.TButton", 
      padding=5, 
      background="#4ebf71", 
      borderwidth=2, 
      relief="flat"
    )
    style.map(
      "success.TButton", 
      background=[
        ("pressed", "#67db8b"),
      ]
    )
    
    style.configure(
      "danger.TButton", 
      padding=5, 
      background="#FA5252", 
      borderwidth=2, 
      relief="flat"
    )
    style.map(
      "danger.TButton", 
      background=[
        ("pressed", "#fc6262"),
      ]
    )
    
    style.configure(
      "primary.TFrame",
      background="#4ebf71",
    )
    style.configure(
      "secondary.TFrame",
      background="#222222",
      borderwidth=2,
      bordercolor="#4ebf71",
    )
    style.configure(
      "primary.TLabel",
      foreground="#4ebf71",
    )
    style.configure(
      "danger.TFrame",
      foreground="#FA5252",
    )