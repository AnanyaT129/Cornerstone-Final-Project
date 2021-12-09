import matplotlib.pyplot as plt

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = ['15:11:31.178764', '15:11:31.179767', '15:11:31.916555', '15:11:32.924060', '15:11:33.909720', '15:11:34.921469', '15:11:35.910000', '15:11:36.910472', '15:11:37.921187', '15:11:38.929070', '15:11:39.929185', '15:11:40.933312', '15:11:41.932674', '15:11:42.912581', '15:11:43.920392', '15:11:44.926365', '15:11:45.927268', '15:11:46.932728', '15:11:47.934687', '15:11:48.915784', '15:11:49.918748', '15:11:50.934565', '15:11:51.912294', '15:11:52.916008', '15:11:53.922822', '15:11:54.933038', '15:11:55.934691', '15:11:56.917357', '15:11:57.921300', '15:11:58.924985']
ys = [0, 148, 0, 0, 0, 0, 0, 210, 204, 211, 208, 156, 197, 212, 215, 210, 208, 212, 210, 211, 0, 207, 0, 146, 206, 211, 210, 0, 209, 139]

# Draw plot
ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('TMP102 Temperature over Time')
plt.ylabel('Temperature (deg C)')

# Draw the graph
plt.show()