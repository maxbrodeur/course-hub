
import sys
import os
import subprocess
import struct

def pn(n=1):
	for i in range(n):
		print('\n', end='')

IFRAME = b'\x00\x00\x01\xb0'
PFRAME = b'\x00\x00\x01\xb6'
VFRAME = b'00dc'
AFRAME = b'01wb'


### ================================================================================================== ###

def num(bdata):
	return int.from_bytes(bdata, 'little')

def byt(ndata):
	return struct.pack('<I', ndata)

def fix(size):
	if size % 2 == 0:
		return size
	else:
		return size + 1

def check_avi(file):
	if file.read(4) != b'RIFF':
		raise IOError('Avi file incorrectly formatted. \'RIFF\' not found.')

	size = num(file.read(4))

	if file.read(4) != b'AVI ':
		raise IOError('Avi file incorrectly formatted. \'AVI \' not found.')

	return size

def read_prev(io, rewind=True):
	io.seek(-4, 1) if rewind else None
	pn()
	print(io.read(4))
	print('pos: {}'.format(io.tell()))
	pn()

def fs(bytes_in):
	print(fourcc(bytes_in, False, True))


def fourcc(bytes_in, integer=False, smart=False, zeroes_num=True):
		ret=[]
		switch = False
		count = 0
		for i in range(0, len(bytes_in), 4):
			curr_bytes = bytes_in[i:i+4]
			if smart:
				if curr_bytes == b'\x00\x00\x00\x00':
					if not switch:
						switch = True
					count += 1
				else:
					if switch:
						switch = False
						if count > 6:
							if zeroes_num:
								ret.append('0 . . . 0 ({})'.format(count))
							else:
								ret.append('0 . . . 0')
						else:
							for i in range(count):
								ret.append(0)
						count = 0
					no_ints = [b'str', b'JUN', b'LIS', b'AVI', b'avi', B'RIF', b'hdr', b'lis', b'vid', b'FMP', b'00d', b'01w', b'aud', b'mov', b'ind', b'idx', b'ixd']
					if curr_bytes[:3] in no_ints:
						to_append = curr_bytes
					else:
						to_append = int.from_bytes(curr_bytes, 'little')
			else:
				if integer:
					to_append = int.from_bytes(curr_bytes, 'little')
				else:
					to_append = curr_bytes

			if curr_bytes != b'\x00\x00\x00\x00' or not smart:
				ret.append(to_append)
		return ret

def get_header(data):
	movi = data.find(b'movi')
	return data[:movi+4]

'''
def get_movi(data):
	movi = data.find(b'movi')
	idx1 = data.find(b'idx1')
	return data[movi+4:idx1]

def get_idx1(data):
	idx1 = data.find(b'idx1')
	return data[idx1:]
'''



def read_bytes(bytes_in, n=4):
	ret = []
	for i in range(0, len(bytes_in), n):
		ret.append(bytes_in[i:i+n])

	return ret



def bytes_to_int(bytes_in, offset=4, smart=False):

	to_return = []

	for i in range(0, len(bytes_in), offset):
		curr_byte = bytes_in[i:i+offset]
		#curr_byte = bytes(curr_byte)
		int_conv = int.from_bytes(curr_byte, 'little')
		to_return.append(int_conv)

	return to_return




def bytes_to_hex(bytes_in, offset=4):

	to_return = []
	for i in range(0, len(bytes_in), offset):
		hex_conv = bytes_in[i:i+offset].hex()
		to_return.append(hex_conv)

	return to_return





def bytes_to_bits(bytes_in):
	return [1 if (bytes_in[i//8] & 1 << i%8 != 0) else 0 for i in range(len(bytes_in) * 8)]

def bytes_to_tf(bytes_in):
	return [bytes_in[i//8] & 1 << i%8 != 0 for i in range(len(bytes_in) * 8)]


### ================================================================================================== ###




def get_fps(file):
		cmd = 'ffprobe {} -v 0 -select_streams v -print_format flat -show_entries stream=r_frame_rate'.format(file)
		fps_pre = os.popen(cmd).read()
		fps_pre = fps_pre.split('=')[1].strip()[1:-1].split('/')
		if len(fps_pre) == 1:
			return float(fps_pre[0])
		elif len(fps_pre) == 2:
			return float(fps_pre[0]) / float(fps_pre[1])
		else:
			return -1




def get_duration_timecode(file):
		os.system("mkdir temp")
		os.system("ffmpeg -i {} 2> temp/temp_vid_info.txt".format(file))
		duration = os.popen("awk \'/Duration:/ { print $2 }\' < temp/temp_vid_info.txt | sed -e \'s/,//\'").read()
		os.system("rm temp/temp_vid_info.txt")
		os.system("rmdir temp")
		#print(duration)
		return duration.strip('\n')




def get_seconds_from_timecode(timecode):
	time_array = timecode.split(':')
	last_element = time_array[-1].split('.')

	if len(time_array) == 3:
		hours = int(time_array[0])
		minutes = int(time_array[1])

		if len(last_element) == 2:
			seconds = int(last_element[0])
			mseconds_pre = last_element[1]
		elif len(last_element) == 1:
			seconds = int(last_element[0])
			mseconds_pre = '0'

	elif len(time_array) == 2:
		hours = '0'
		minutes = int(time_array[0])

		if len(last_element) == 2:
			seconds = int(last_element[0])
			mseconds_pre = last_element[1]
		elif len(last_element) == 1:
			seconds = int(last_element[0])
			mseconds_pre = '0'

	else:
		raise ValueError("Timecode incorrectly formatted. Need either HH:MM:SS or MM:SS (milliseconds optional).")

	if len(mseconds_pre) == 3:
		k = 1000.0
	elif len(mseconds_pre) == 2:
		k = 100.0
	elif len(mseconds_pre) == 1:
		k = 10.0
	else:
		raise ValueError("Milliseconds incorrectly formatted. Need: (HH:)MM:SS.m or .mm or .mmm or none.")

	h_to_s = float(hours * 3600)
	m_to_s = float(minutes * 60)
	ms_to_s = float(mseconds_pre) / k


	return h_to_s + m_to_s + seconds + ms_to_s




def get_duration(file):
	timecode = get_duration_timecode(file)
	return get_seconds_from_timecode(timecode)



### ================================================================================================== ###



def get_frame_count(data):
	h = data.find(b'avih')
	frames_bytes = data[h+(6*4):h+(6*4)+4]
	print('frames_bytes: {}'.format(frames_bytes))
	print('frames: {}'.format(int.from_bytes(frames_bytes, 'little')))

	before_idx1 = data.split(b'idx1')
	after_movi = before_idx1[0].split(b'movi')
	frame_split = after_movi[1].split(b'00dc')
	print(len(frame_split))

def check_idx1(data):
	m = data.find(b'movi')
	idx1_pos = data[m-4:m]
	numb = int.from_bytes(idx1_pos, 'little')
	print('idx1pos: {}'.format(numb))
	i = data.find(b'idx1')
	print('idx1 pos\'n - movi: {}'.format(i - m))
	print(data[num(idx1_pos):num(idx1_pos)+4])

def get_idx1(data, max=None):
	i = data.find(b'idx1')
	part = data[i:]
	if max==None:
		print(fourcc(part, smart=True))
	else:
		print(fourcc(part[:max], smart=True))

def get_movi(data, max=None):
	m = data.find(b'movi')
	if max == None:
		max = data.find(b'idx1')
	part = data[m:]
	print(fourcc(part[:max], smart=True))



### ================================================================================================== ###

'''
ffmpeg version 4.4 Copyright (c) 2000-2021 the FFmpeg developers
  built with Apple clang version 12.0.0 (clang-1200.0.32.29)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.4_1 --enable-shared --enable-pthreads --enable-version3 --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libdav1d --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox
  libavutil      56. 70.100 / 56. 70.100
  libavcodec     58.134.100 / 58.134.100
  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  9.100 /  5.  9.100
  libswresample   3.  9.100 /  3.  9.100
  libpostproc    55.  9.100 / 55.  9.100
'''












