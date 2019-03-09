column_l = 617  # left and sample column
column_r = 1190  # right and sample column

last_delta = 2000  # after last page, give additional print
min_delta = 10  # min frames delta between 2 print
min_line_delta = 3 # min 2 line between sample, if screen flash
min_color = 3  # white or black, sum(RGB)



from moviepy.editor import VideoFileClip
from PIL import Image

clip1 = VideoFileClip('./sample/sample_input.mp4')
i = 1
last = -1-min_delta
ii = 0
last_a = 0
#len_v = len(list(clip1.iter_frames()))
for frame in clip1.iter_frames():
	data = [j[column_l] for j in frame]
	flag = "w"
	count = 0
	c = [-1]
	for j in range(len(data)):
#		print(d, d[0]+d[1]+d[2])
		if sum(data[j]) > min_color and flag == "w" and j > c[-1]+min_line_delta:
			count += 1
			flag = "b"
			c.append(j)
		elif sum(data[j]) < min_color and flag == "b" and j > c[-1]+min_line_delta:
			count += 1
			flag = "w"
			c.append(j)
	if count > 5:  # try more if not work
		if i <= last+min_delta:
			last = i
		else:
			last = i
			frame = frame[c[2]:c[5]]  # may be need to adapt for COUNT
			last_a = c[5]-c[2]  # may be need to adapt for COUNT
			im = Image.fromarray(frame)
			im = im.crop((column_l, 0, column_r, last_a))
			im.save("./sample/sample_images/frame_%03d.jpg" % (ii))  # create dir manually if error
			print(ii, "- Print", i)
			ii += 1
	if i == last+last_delta:
		frame = frame[c[2]:c[2]+last_a]
		im = Image.fromarray(frame)
		im = im.crop((column_l, 0, column_r, last_a))
		im.save("./sample/sample_images/frame_%03d.jpg" % (ii))
		print(ii, "- Last print", i)
		ii += 1
		break
	i = i+1