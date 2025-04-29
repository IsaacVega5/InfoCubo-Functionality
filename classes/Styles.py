
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