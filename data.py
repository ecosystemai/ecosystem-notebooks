import networkx as nx
import mongo_connector
import math 
import datetime
from dateutil.relativedelta import relativedelta

def curvepoint(x1, y1, x2, y2):
	x3 = min(x1, x2) + abs(x1 - x2)/2
	y3 = min(y1, y2) + abs(y1 - y2)/2
	lsqr = ((x1 - x3)**2 + (y1 - y3)**2) * 0.05
	m = (y1 - y2)/(x1 - x2)
	inv_m = (-1)/m
	xsqr = lsqr/(1+(inv_m**2))
	delx = math.sqrt(xsqr)
	dely = inv_m*delx
	x4 = x3 + delx
	y4 = y3 + dely
	return [x4, y4]

class DataReader:
	def __init__(self):
		# g = nx.read_gml("netscience.gml")
		# conn = mongo_connector.FilteredTransactionReader(500, [2018, 7, 1], [2018, 8, 20], [])
		# conn = mongo_connector.TransactionReader(200)
		conn = mongo_connector.TransactionReader(5)
		print("Reading User Data")
		nu = conn.get_unique_users()
		print("Reading Transaction Type Data")
		# nt = conn.get_unique_transaction_types()
		nt = ["Contribution Credit Cash", "Contribution Debit Cash", "Contribution Schedule Investment"]

		self.nu = nu
		self.all_nu = nu
		self.nt = nt

		g = nx.Graph()
		self.current_g = g
		g.add_nodes_from(nu)
		g.add_nodes_from(nt)

		counter = 0
		print("Reading Edge Data")
		while True:
		# for i in range(10):
			print(counter)
			counter += 1
			re = conn.read()
			read = False
			for entry in re:
				read = True
				# Format Example: Aug 10 2018 12:00:00:000AM
				try:
					dt = datetime.datetime.strptime(entry["DATE_TIME"], "%b %d %Y %I:%M:%S:%f%p")
					g.add_edge(entry["USER"], entry["TYPE"], date=dt)
				except:
					pass

			if not read:
				break
			if counter >= 10:
				break

		self.edges = g.edges()
		self.edges_dt = []
		for edge in self.edges:
			self.edges_dt.append(g.get_edge_data(edge[0], edge[1])["date"])
		print("Applying Layout")
		# circular_layout(G[, scale, center, dim])
		# kamada_kawai_layout(G[, dist, pos, weight, …])
		# planar_layout(G[, scale, center, dim])
		# random_layout(G[, center, dim, seed])
		# shell_layout(G[, nlist, rotate, scale, …])
		# spring_layout(G[, k, pos, fixed, …])
		# spectral_layout(G[, weight, scale, center, dim])
		# spiral_layout(G[, scale, center, dim, …])
		# multipartite_layout(G[, subset_key, align, …])
		self.pos = nx.fruchterman_reingold_layout(g)
		print("Layout Applied")
		print("Applying Algorithms")
		self.betweenness_centrality = []
		self.closeness_centrality = []
		print("Algorithms Applied")

	def getClosenessCentrality(self):
		return nx.algorithms.centrality.closeness_centrality(self.current_g)

	def getBetweennessCentrality(self):
		# for edge in self.current_g.edges():
		# 	print(edge)
		return nx.algorithms.centrality.betweenness_centrality(self.current_g)

	def getEarliestDate(self):
		return min(self.edges_dt).strftime("%Y-%m-%d")

	def getLatestDate(self):
		return max(self.edges_dt).strftime("%Y-%m-%d")

	def getDates(self):
		return self.edges_dt

	def getLatestDateM1M(self):
		return (max(self.edges_dt) + relativedelta(months=-1)).strftime("%Y-%m-%d")

	def getLatestDateP1(self):
		return (max(self.edges_dt) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

	def getPos(self):
		return self.pos

	def getAllNu(self):
		return self.all_nu

	def getNu(self):
		return self.nu

	def getNt(self):
		return self.nt

	def getEdges(self):
		return self.edges

	def getEdgeCount(self):
		return self.edge_counts

class DataFilter:
	def __init__(self, pos):
		self.pos = pos

	def getClosenessCentrality(self):
		return nx.algorithms.centrality.closeness_centrality(self.current_g)

	def getBetweennessCentrality(self):
		# for edge in self.current_g.edges():
		# 	print(edge)
		return nx.algorithms.centrality.betweenness_centrality(self.current_g)

	def getEarliestDate(self):
		return min(self.edges_dt).strftime("%Y-%m-%d")

	def getLatestDate(self):
		return max(self.edges_dt).strftime("%Y-%m-%d")

	def getDates(self):
		return self.edges_dt

	def getLatestDateM1M(self):
		return (max(self.edges_dt) + relativedelta(months=-1)).strftime("%Y-%m-%d")

	def getLatestDateP1(self):
		return (max(self.edges_dt) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

	def getPos(self):
		return self.pos

	def getAllNu(self):
		return self.all_nu

	def getNu(self):
		return self.nu

	def getNt(self):
		return self.nt

	def getEdges(self):
		return self.edges

	def getEdgeCount(self):
		return self.edge_counts


	def filter(self, dropdown_value, start_date, end_date):
		start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
		# print("----------------------------------------------")
		# print(dropdown_value)
		conn = mongo_connector.FilteredTransactionReader(500, [start_date.year, start_date.month, start_date.day], [end_date.year, end_date.month, end_date.day], dropdown_value)
		# conn = mongo_connector.FilteredTransactionReader(500, [2018, 7, 1], [2018, 8, 20], [])
		# self.nt = ["Contribution Credit Cash", "Contribution Debit Cash", "Contribution Schedule Investment"]

		g = nx.Graph()
		self.edges = []
		self.edge_counts = []
		counter = 0
		print("Reading Edge Data")
		while True:
		# for i in range(10):
			print(counter)
			counter += 1
			re = conn.read()
			read = False
			for entry in re:
				read = True
				# Format Example: Aug 10 2018 12:00:00:000AM
				try:
					dt = datetime.datetime.strptime(entry["DATE_TIME"], "%b %d %Y %I:%M:%S:%f%p")
					# print("Adding: {}:{}".format(entry["USER"], entry["TYPE"]))
					if not g.has_edge(entry["USER"], entry["TYPE"]):
						g.add_edge(entry["USER"], entry["TYPE"], date=dt)
					if [entry["USER"], entry["TYPE"]] not in self.edges:
						self.edges.append([entry["USER"], entry["TYPE"]])
						self.edge_counts.append(1)
					else:
						self.edge_counts[self.edges.index([entry["USER"], entry["TYPE"]])] += 1

				except:
					pass

			if not read:
				break
			# if counter >= 10:
				# break
				
		print("Reading User Data")
		self.nu = conn.get_unique_users()
		print("Reading Transaction Type Data")
		self.nt = conn.get_unique_transaction_types()
		g.add_nodes_from(self.nu)
		g.add_nodes_from(self.nt)

		self.current_g = g

		print("edge count: {}".format(len(self.edges)))

		print("{}->{}".format(start_date, end_date))
		pos = self.pos

		output = {
			"nu_xv": [],
			"nu_yv": [],
			"nt_xv": [],
			"nt_yv": [],
			"Xed": [],
			"Yed": [],
			"edge_names": [],
			"nu_names": [],
			"nt_names": []
		}
		output["nu_names"] = dropdown_value

		if "__all_transaction_types__" in dropdown_value:
			output["nt_xv"] = [pos[k][0] for k in self.nt]
			output["nt_yv"] = [pos[k][1] for k in self.nt]
			output["nt_names"] = self.nt
			output["nu_names"].remove("__all_transaction_types__")

		# filtered_edges = []

		# for i, edge in enumerate(self.edges):
		# 	if edge[0] in dropdown_value:
		# 		if edge[1] in self.nt:
		# 			filtered_edges.append(edge)
		new_counts = []
		# for edge in self.edges:
		for i, edge in enumerate(self.edges):
			cp = curvepoint(pos[edge[0]][0], pos[edge[0]][1], pos[edge[1]][0], pos[edge[1]][1])
			output["Xed"] += [pos[edge[0]][0], cp[0], pos[edge[1]][0], None]
			output["Yed"] += [pos[edge[0]][1], cp[1], pos[edge[1]][1], None]
			for j in range(4):
				output["edge_names"].append([edge[0], edge[1]])
				new_counts.append(self.edge_counts[i])
		self.edge_counts = new_counts

		if "__all_transaction_types__" not in dropdown_value:
			for nt in self.nt:
				output["nt_xv"] += [pos[nt][0]]
				output["nt_yv"] += [pos[nt][1]]
				output["nt_names"].append(nt)

		for val in dropdown_value:
			if val != "__all_transaction_types__":
				output["nu_xv"].append(pos[val][0]),
				output["nu_yv"].append(pos[val][1]),

		return output