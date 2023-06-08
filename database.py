from supabase import create_client
import haversine as hs
import os


def closestLocation(qrcode):
    
  url = os.environ['url']
  key = os.environ['key']
    
  supabase = create_client(url, key)

  try:
    customerLocations = supabase.table("QR Codes").select("Latitude", "Longitude").eq("QR Code", qrcode).execute()
  except:
    return "QR Code not found..."
    
  volunteerLocations = supabase.table("Volunteer Locations").select("Latitude", "Longitude", "Location Name").execute()
    
    
  closestLocation = {"name": "", "distance": 0}
  
  for customerLocation in customerLocations.data:
    for volunteerLocation in volunteerLocations.data:
      customer_location = (customerLocation["Latitude"], customerLocation["Longitude"])
      volunteer_location = (volunteerLocation["Latitude"], volunteerLocation["Longitude"])
      distance = hs.haversine(customer_location, volunteer_location)
      if closestLocation["distance"] > distance or closestLocation["distance"] == 0:
        closestLocation["distance"] = distance
        closestLocation["name"] = volunteerLocation["Location Name"]
        
    return closestLocation["name"]

def inventoryCount(locoName, orderList):
  unavailableItems = []
  itemNum = 0
  url = os.environ['url']
  key = os.environ['key']
    
  supabase = create_client(url, key)

  inventory = supabase.table("Inventory").select("*").eq("Location Name", locoName).execute()
  inv = inventory.data[0]
  del inv["Location Name"]
  del inv["Customer Count"]
  for item in inv:
    if inv[item] < orderList[itemNum]:
      unavailableItems.append(f'{item} - ({inv[item]} left)')
    itemNum+=1 
  print(f"Your order request does not meet our current supply for these items: {unavailableItems}")

def purchase(locoName, qrcode, cost, orderList):
  itemNum = 0
  url = os.environ['url']
  key = os.environ['key']
    
  supabase = create_client(url, key)

  inventory = supabase.table("Inventory").select("*").eq("Location Name", locoName).execute()
  customerSettings = supabase.table("QR Codes").select("*").eq("QR Code", qrcode).execute()
  inv = inventory.data[0]
  del inv["Location Name"]
  inv["Customer Count"]+=1
  customerCount = supabase.table("Inventory").update({"Customer Count":inv["Customer Count"]}).eq("Location Name", locoName).execute()
  del inv["Customer Count"]
  for item in inv:
    inv[item] = inv[item]-orderList[itemNum]
    itemNum+=1
  newInventory =     supabase.table("Inventory").update(inv).eq("Location Name", locoName).execute()
  
    
  
   
        
  

