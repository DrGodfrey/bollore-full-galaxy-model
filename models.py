from collections import Counter

# # example of use
# counter1 = Counter({'a': 2.5, 'b': 5.0})
# counter2 = Counter({'a': 3.1, 'c': 7.2})

# result = counter1 + counter2


class Galaxy_company:
    def __init__(self, name, owned_by={}, direct_assets={}, is_outside=False):
        self.name = name
        
        if is_outside: 
            # sets company as outside company if specified
            self.is_outside = is_outside #tag to identify outside holding entities (treat outside shareholders as company)
        else:
            # if company has no owners set it to an outside company
            if owned_by == {}:
                self.is_outside = True
            else:
                # Otherwise allow it to default to False (default)
                self.is_outside = is_outside 
        
        
        self.owned_by = Counter(owned_by) #who to distribute to -> zero for outside (dict)
        self.direct_assets = Counter(direct_assets) #distribute these     
        
        #initialise:        
        self.economic_ownership = Counter(direct_assets) #this will eventually be distributed to outside shareholders!
        self.new_assets = Counter({}) # this will store assets as they're distributed each cycle
    
    def distribute(self, companies):
        # Distribute the assets to the owners based on their ownership fractions
        for owner, percentage in self.owned_by.items():
            # Find the company object for the owner
            owner_company = next((company for company in companies if company.name == owner), None)
            
            if owner_company is None: raise ValueError(f"Company '{owner}' not found in the list of companies.")
            
            # Calculate the assets to transfer to the owner
            distribution = Counter({asset: value * percentage/100 for asset, value in self.economic_ownership.items()})
            
            # Add the distributed assets to the owner's `new_assets`
            owner_company.new_assets += distribution

        # Just distributed 'economic_ownership' so zero this unless the company is an
        # outside company (ie no owners) and didn't distribute
        if not self.is_outside: self.economic_ownership = Counter({}) 
    
    def initialise_cycle(self):
        # once all companies have distributed assets, this will re-initialise
        # in order to allow cycle to restart
        self.economic_ownership = self.economic_ownership + self.new_assets
        self.new_assets = Counter({})
    

        
        
    
# bollore_o = Galaxy_company(name='bollore_o', is_outside=True)
# odet_o = Galaxy_company(name='odet_o', is_outside=True)

# bollore_owned_by = {
#     "odet":0.7,
#     "bollore_o":0.3
# }

# bollore_direct_assets = {
#     "UMG": 7,
#     "Cash": 6
# }

# bollore = Galaxy_company(name='bollore', owned_by=bollore_owned_by, direct_assets=bollore_direct_assets)

# odet_owned_by = {
#     "bollore":0.84,
#     "odet_o":0.16
# }

# odet = Galaxy_company(name='odet', owned_by=odet_owned_by)

# companies = [bollore_o, odet_o, bollore, odet]

# for i in range(0,1):
#     for company in companies:
#         company.distribute(companies)
        
#     for company in companies:
#         company.initialise_cycle()
    
#     for company in companies:
#         print(company.name,":", company.economic_ownership)


companies_list = [
    "Bolloré Participations SE", #family holdings
    "Omnium Bolloré",
    "Financière V",
    "Sofibol",
    # to side of diagram
    "Compagnie des Deux Cœurs",
    ## MAIN
    "Compagnie de l'Odet",
    "Bolloré SE",
    # Ex-Rivaud
    "Plantations des Terres Rouges",
    "Compagnie du Cambodge",
    "Financière Moncey",
    "Société Industrielle et Financière de l'Artois",
    # 2nd line Ex-Rivaud
    "Société des Chemins de Fer et Tramways du Var et du Gard",
    "Compagnie des Tramways de Rouen",
    "Société Bordelaise Africaine",
    # 3rd line Ex-Rivaud
    "La Forestière Équatoriale",
    
    # not shown directly on diagram
    "Financière du Champ de Mars",              
    "Compagnie Saint Gabriel",
    "Imperial Mediterranean",
    "Nord-Sumatra Investissements", 
         
    "Compagnie de Guénolé",
    "Socfrance",
]

assets = [
    "Vivendi SE",
    "Bolloré Energy",
    "Bolloré Logistics",
    "Universal Music Group",
    "Blue Systems"
]



companies = {
    # company name                # owned by - if empty - outside shareholder
    "Bolloré Participations SE": {}, #family holdings
    "Compagnie de l'Odet Outsiders": {},
    "Bolloré SE Outsiders": {},
    "Compagnie du Cambodge Outsiders": {},
    "Financière Moncey Outsiders": {},
    "Société Industrielle et Financière de l'Artois Outsiders": {},
    "Compagnie des Tramways de Rouen Outsiders": {},
    "Société des Chemins de Fer et Tramways du Var et du Gard Outsiders": {},
    "La Forestière Équatoriale Outsiders": {},
    
    # not shown directly on diagram
    "Socfrance Outsiders": {},
    "SFA Outsiders": {},
    
    
    "Omnium Bolloré": {
        "Bolloré Participations SE": 50.2, 
        "Financière du Champ de Mars": 27.9, #"Bolloré SE" 100%
        "Financière Moncey": 17.1,
        "Bolloré SE": 4.8
    },
    "Financière V": {
        "Omnium Bolloré": 50.3,
        "Compagnie du Cambodge": 22.8,
        "Financière Moncey": 10.5,
        "Bolloré SE": 10.3,
        "Société Industrielle et Financière de l'Artois": 4.0,
        "Compagnie des Tramways de Rouen": 1.7,
        "Société des Chemins de Fer et Tramways du Var et du Gard": 0.4
    },
    "Sofibol": {
        "Financière V": 51.1,
        "Bolloré SE": 35.9,
        "Compagnie Saint Gabriel": 13.0 #Bolloré SE" 99.99%
    },
    # to side of diagram
    "Compagnie des Deux Cœurs": {
        "Sofibol": 49.0,
        "Bolloré Participations SE": 51.0
    },
    ## MAIN
    "Compagnie de l'Odet": {
        "Compagnie de l'Odet Outsiders": 6.9,  # Combined internal + external ownership
        "Sofibol": 56.1,
        "Compagnie du Cambodge": 19.1,
        "Société Industrielle et Financière de l'Artois": 5.6,
        "Financière Moncey": 4.9,
        "Imperial Mediterranean": 3.8,
        "Nord-Sumatra Investissements": 2.3,
        "Bolloré Participations SE": 0.9,
        "Compagnie des Deux Cœurs": 0.4
    },
    "Bolloré SE": {
        "Bolloré SE Outsiders": 30.1,
        "Compagnie de l'Odet": 69.4,
        "Bolloré SE": 0.5 # Sociétés contrôlées par Bolloré SE:
        #Imperial Mediterranean 99%, Société Bordelaise Africaine - see entry and Nord-Sumatra Investissements 100.00%.
        
    },
    
    # 100% owned by Bollore?
    "Financière du Champ de Mars": {"Bolloré SE": 100},
    "Compagnie Saint Gabriel": {"Bolloré SE": 99.99},
    "Imperial Mediterranean": {"Bolloré SE": 99.00},
    "Nord-Sumatra Investissements": {"Bolloré SE": 100},
    
    # Ex-Rivaud
    "Plantations des Terres Rouges": {
        "Bolloré SE": 67.2,
        "Compagnie du Cambodge": 10.0,
        "Société Industrielle et Financière de l'Artois": 22.8   
    },
    # SFA, not shown in diagram, but 98.4% subsitdiary of S. Plantations des Terres Rouges
    "SFA":{
        "SFA Outsiders": 100 - 98.4,
        "Plantations des Terres Rouges": 98.4
    },
    
    "Compagnie du Cambodge": {
        "Compagnie du Cambodge Outsiders": 0.8,
        "Bolloré SE": 37.0,
        "Plantations des Terres Rouges": 62.2
    },
    "Financière Moncey": {
        "Financière Moncey Outsiders": 3.7,
        "Bolloré SE": 15.3,
        "Compagnie du Cambodge": 36.7,
        "Société des Chemins de Fer et Tramways du Var et du Gard": 26.6,
        "Plantations des Terres Rouges": 17.5
    },
    "Société Industrielle et Financière de l'Artois": {
        "Société Industrielle et Financière de l'Artois Outsiders": 4.2,
        "Bolloré SE": 9.3,
        "Compagnie du Cambodge": 7.4,
        "Financière Moncey": 42.1,
        "Société Bordelaise Africaine": 30.2,
        "Socfrance": 6.8  
    },
    # 2nd line Ex-Rivaud
    "Société des Chemins de Fer et Tramways du Var et du Gard": {
        "Société des Chemins de Fer et Tramways du Var et du Gard Outsiders": 3.7,
        "Compagnie du Cambodge": 31.5,
        "Socfrance": 64.8
    },
    "Compagnie des Tramways de Rouen": {
        "Compagnie des Tramways de Rouen Outsiders": 6.0,
        "Financière Moncey": 48.1,
        "Plantations des Terres Rouges": 3.3,
        "Société des Chemins de Fer et Tramways du Var et du Gard": 14.0,
        "Compagnie du Cambodge": 28.6   
    },
    "Société Bordelaise Africaine": { 
        # !!! 0.5% seems to be missing from diagram !!!
        "Bolloré SE": 90.5,
        "La Forestière Équatoriale": 8.9,   
    },
    # Socfrance, not shown in diagram, but 53.6% subsitdiary of S. Boredelaise Africaine
    "Socfrance": {
        "Socfrance Outsiders": 100 - 97.36,
        "Bolloré SE": 97.36 - 53.6, #Bollore report has ownership at 97.36% total (so this would be rest of ownership stake)
        "Société Bordelaise Africaine": 53.6
    },
    # 3rd line Ex-Rivaud
    "La Forestière Équatoriale": {
        "La Forestière Équatoriale Outsiders": 2.2,
        "Bolloré SE": 29.2,
        "Compagnie du Cambodge": 64.5,
        "SFA": 4.1 
        
    },
}




# for company_name in companies_list:
#     print(company_name, sum([share for company, share in companies[company_name].items()])) # check that this adds up to 100




bollore_direct_assets = {
    # Units = M
    "UMG": 7.5 * 1000,
    "Cash": 6.1 * 1000,
    "Vivendi": 3.4 * 1000
}
galaxy_list = [] 
for company_name, owned_by in companies.items():
    if company_name == "Bolloré SE":
        galaxy_list += [ Galaxy_company(name=company_name, owned_by= owned_by, direct_assets=bollore_direct_assets) ]
    else: galaxy_list += [ Galaxy_company(name=company_name, owned_by= owned_by) ]


for i in range(0,500):
    for company in galaxy_list:
        company.distribute(galaxy_list)
    
    for company in galaxy_list:
        company.initialise_cycle()

for company in galaxy_list[0:10]:
        print(company.name,":", company.economic_ownership)









class Company:   
    def __init__(self, name, shares_outstanding, shareprice, currency='€'):
        self.name = name
        self.shares_outstanding = shares_outstanding
        self.shareprice = shareprice
        self.currency = currency

        #initialising values
        self.assets = []
        self.value = 0  
        self.discount_to_value_percent = 0
        self.outputs = {'assets': []}

        #updates .outputs with formatted values
        self.update_outputs()
     
    def market_cap(self, to_string=False):
        mkt_cap = self.shares_outstanding * self.shareprice
        if to_string:
            mkt_cap = Company.large_number_to_string(mkt_cap)
        return mkt_cap
    
    def asign_asset(self, asset, value='optional', is_company_object=False, ownership_fraction=1):
        if is_company_object:
            value_of_asset = asset.market_cap() * ownership_fraction
            name_of_asset = asset.name
        else:
            value_of_asset = value
            name_of_asset = asset
        
        self.assets += [{
            'name': name_of_asset,
            'ownership_percentage': ownership_fraction,
            'value': value_of_asset
            }]
        self.outputs['assets'] += [{
            'name': name_of_asset,
            'ownership_percentage': Company.fraction_to_percentage_string(ownership_fraction),
            'value': Company.large_number_to_string(value_of_asset)
            }]    
        self.value += value_of_asset
        self.discount_to_value_percent = Company.fraction_to_percentage_string(1 - (self.market_cap() / self.value))        
        self.update_outputs()

    def update_outputs(self):
        new_outputs = {
            'name': self.name,
            'title': str(self),
            'market_cap': self.market_cap(to_string=True),
            'shares_outstanding': Company.large_number_to_string(self.shares_outstanding),
            'value': Company.large_number_to_string(self.value),
            'currency': self.currency,
            'share_price': self.shareprice
        }
        self.add_output(new_outputs)

    def add_output(self, new_outputs):
        self.outputs.update(new_outputs)

    def __str__(self):
        return f'{self.name} (mkt cap {self.market_cap(to_string=True)} @ {self.shareprice} per share)'
    
    @staticmethod
    def large_number_to_string(value):
        if value > 1000000000:
            value = f"{str(round(value/1000000000,1))}B"
        else:
            value = f"{str(int(round(value/1000000,0)))}M"
        return value
    
    @staticmethod
    def fraction_to_percentage_string(value):
        percentage_string = ''
        if value > 0.10:
            percentage_string = f'{int(round(value * 100, 0))}%'
        else:
            percentage_string = f'{round(value * 100, 1)}%'
        return percentage_string




import networkx as nx
import matplotlib.pyplot as plt

visualise_network = False
if visualise_network:
    # Initialize a directed graph
    G = nx.DiGraph()

    # Add nodes and edges based on the dictionary
    for company, ownerships in companies.items():
        for owned_company, percentage in ownerships.items():
            G.add_edge(company, owned_company, weight=percentage)

    # Set positions for all nodes in the graph
    pos = nx.spring_layout(G, k=10, iterations=100) # Spring layout for better visualization

    # Draw the nodes and edges with labels
    plt.figure(figsize=(12, 12))

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=300, node_color="lightblue", font_size=6, font_weight="bold", arrows=True)

    # Draw edge labels (ownership percentages)
    edge_labels = {(u, v): f"{d['weight']}%" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Show plot
    plt.title("Company Ownership Diagram")
    plt.show()


# # Initialize a directed graph
# G = nx.DiGraph()

# # Add nodes and edges based on the dictionary
# for company, ownerships in companies.items():
#     for owned_company, percentage in ownerships.items():
#         G.add_edge(company, owned_company, weight=percentage)

# # Set positions for nodes using Kamada-Kawai layout
# pos = nx.kamada_kawai_layout(G)

# # Apply a scaling factor to the positions to increase spacing
# scaling_factor = 2  # Adjust this value to control the spacing
# for key in pos:
#     pos[key] *= scaling_factor

# # Draw the nodes and edges with labels
# plt.figure(figsize=(12, 12))

# # Draw nodes and edges
# nx.draw(G, pos,  with_labels=True, node_size=300, node_color="lightblue", font_size=5, font_weight="bold", arrows=True)

# # Draw edge labels (ownership percentages)
# edge_labels = {(u, v): f"{d['weight']}%" for u, v, d in G.edges(data=True)}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# # Show plot
# plt.title("Company Ownership Diagram - Kamada Kawai Layout")
# plt.show()


# from py2cytoscape.data.cyrest_client import CyRestClient
# import networkx as nx

# # Initialize the CyRestClient to interact with Cytoscape
# cy = CyRestClient()

# # Create a sample graph in NetworkX
# G = nx.DiGraph()

# # Add edges from the companies dictionary
# for company, ownerships in companies.items():
#     for owned_company, percentage in ownerships.items():
#         G.add_edge(company, owned_company, weight=percentage)

# # Convert NetworkX graph to a Cytoscape-compatible format
# cy_edges = [{"data": {"source": u, "target": v, "weight": d['weight']}} for u, v, d in G.edges(data=True)]
# cy_nodes = [{"data": {"id": node}} for node in G.nodes()]

# cy_network = {"data": {"name": "Company Ownership Network"}, "elements": {"nodes": cy_nodes, "edges": cy_edges}}

# # Send the network to Cytoscape
# cy.network.create(cy_network)

# # Apply a layout (e.g., force-directed layout)
# cy.layout.apply(name='force-directed')

# # Apply a visual style (optional)
# cy.style.apply(style_name='default')

# print("Network sent to Cytoscape!")
