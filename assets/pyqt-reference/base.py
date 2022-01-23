from tech import *
from frame import *
from os import path
import random

debug = False
force_idx1 = True
ignore_empty_frames = False


class PyMosh:

	class Header:
		
		def create(filen):
			file = open(filen, 'rb')
			#data = file.read()

			file.seek(0, 0) # 0 absolute, 1 curr pos, 2 from end
			size = check_avi(file)

			movi_pos = 0
			idx1_pos = 0

			# Look for 'movi'.
			# Also make sure we first hit LIST or JUNK chunks
			while True:
				if file.tell() == (size+8):
					raise IOError('Avi incorrectly formatted. Could not find \'movi\'.')

				fourcc = file.read(4)

				read_prev(file) if debug else None

				if fourcc != b'LIST' and fourcc != b'JUNK':
					raise IOError('Avi incorrectly formatted. JUNK or LIST chunks improperly placed.')

				file.seek(4, 1)
				fourcc = file.read(4)

				if fourcc == b'movi':
					movi_pos = file.tell() - 4
					file.seek(-8, 1)
					idx1_pos = num(file.read(4))
					file.seek(idx1_pos, 1)
					if file.read(4) != b'idx1' and force_idx1:
						raise IOError('Avi incorrectly formatted. \'idx1\' not found.')
					break

				file.seek(-8, 1)

				next = num(file.read(4))
				print(next) if debug else None
				file.seek(next, 1)

			file.seek(0, 0)
			header = PyMosh.Header(filen, file.read(movi_pos+4), movi_pos)

			curr = file.read(4)

			while curr == b'01wb':
				curr_size = fix(num(file.read(4)))
				file.seek(curr_size + (curr_size%2), 1)
				curr = file.read(4)


			if curr != b'00dc':
				read_prev(file) if debug else None
				raise IOError('Avi incorrectly formatted or empty. No frames found.')

			empty_offset = 0
			index_frames = []
			while curr == b'00dc':
				start = file.tell() - 4
				curr_size = fix(num(file.read(4)))
				frame_size = curr_size

				flag_check = file.read(4)
				if flag_check != IFRAME and flag_check != PFRAME:
					keyframe = None # None means BFRAME
				else:
					keyframe = flag_check == IFRAME

				bframe = file.read(1).hex()[0] == '9' and not keyframe
				
				file.seek(-9, 1)

				file.seek(curr_size + 4 + (curr_size%2), 1)
				curr = file.read(4)

				while curr == b'01wb':
					curr_size = fix(num(file.read(4)))
					file.seek(curr_size + (curr_size%2), 1)
					curr = file.read(4)

				end = file.tell() - 4

				if frame_size == 0 and ignore_empty_frames:
					empty_offset += 1
				else:
					index_frame = IndexFrame(start, end, keyframe, bframe, frame_size == 0)
					index_frames.append(index_frame)

			header.frames = index_frames
			if ignore_empty_frames:
				frame_count = num(header.frame_count) - empty_offset
				if frame_count < 0:
					raise ValueError('Empty frames count greater than total frame count in header.')
			header.frame_count = byt(num(header.frame_count) - empty_offset)

			return header

		def __init__(self, filen, data, movi_pos):
			self.file_name = filen
			self.movi_pos = movi_pos
			self.raw = data
			self.total_size = data[4:8]
			self.us_per_frame = data[8*4:8*4 + 4]
			self.frame_count = data[12*4:12*4 + 4]
			self.width = data[16*4:16*4 + 4]
			self.height = data[17*4:17*4 + 4]

			self.FMP4_pos = data.find(b'FMP4')
			if self.FMP4_pos == -1:
				raise IOError('Video is not not encoded in MPEG-4.')
			self.auds_pos = data.find(b'auds')
			self.audio_count = data[self.auds_pos:self.auds_pos+4]

			# audio_frames num: auds_pos + (9 * 4)
			#
			# video_frames num:
			#	1) 12*4
			#	2) FMP4_pos + 7*4
			#
			# idx1 pos num: self.raw[-8:-4]
			#
			# size num: 4

			self.fps = 1 / (num(self.us_per_frame)*1e-06)
			self.length = num(self.frame_count) / self.fps
			self.frames = []

		def __getitem__(self, index):
			return self.frames[index]

		def __len__(self):
			return len(self.frames)

		def as_frame(self, index):
			if isinstance(index, int):
				idx_frame = self.frames[index]
			elif isinstance(index, IndexFrame):
				idx_frame = index
			start = idx_frame.start + 4
			size = idx_frame.size

			fileobj = open(self.file_name, 'rb')
			fileobj.seek(start, 0)
			data = fileobj.read(size)
			#print(data)
			fileobj.close()

			return Frame(data)


		def copy(self):
			return PyMosh.Header(self.file_name, self.raw[:], self.movi_pos)

		def update(self, video_count, audio_count, movi_size):
			idx1_size = 8 + 16*video_count + 16*audio_count
			total_size = len(self.raw)-8 + movi_size + idx1_size

			self.total_size = byt(total_size)
			self.frame_count = byt(video_count)
			self.audio_count = byt(audio_count)
			mv_bytes = byt(movi_size+4) # since we include 'movi' in header, but we already
										# calculated len(input.raw)

			self.raw = self.raw[0:4] + self.total_size + self.raw[8:12*4] + \
			self.frame_count + self.raw[13*4:self.FMP4_pos + 7*4] + self.frame_count + \
			self.raw[self.FMP4_pos + 8*4:self.auds_pos + 8*4] + self.audio_count + \
			self.raw[self.auds_pos + 9*4:-8] + mv_bytes + b'movi'




	### ===================== OPEN/SAVE METHODS ============================ ###



	def __init__(self, header, frames):
		self.header = header
		self.frames = frames

	def empty(self):
		new_header = self.header.copy()
		return PyMosh(new_header, [])

	def create_empty_video(header):
		return PyMosh(header.copy(), [])

	def open(filen):
		header = PyMosh.Header.create(filen)
		video_frames = [header.as_frame(f) for f in header.frames]
		return PyMosh(header, video_frames)


	### ====================== ARRAY IMITATION ====================== ###

	def __getitem__(self, index):
		return self.frames[index]

	def __setitem__(self, index, frame):
		if not isinstance(index, int):
			raise TypeError('Setting an item requires an integer index.')
		if frame == None:
			self.frames.pop(index)
		else:
			self.frames[index] = frame

	def __len__(self):
		return len(self.frames)


	def append(self, frame):
		self.frames.append(frame.copy())

	def append_no_copy(self, frame):
		self.frames.append(frame)



	### ==================== BUILD METHODS ======================= ###


	def get_movi_size(self):
		size = 0 # exclude length of movi since in header class
		for f in self.frames:
			size += len(f)
		return size

	def get_audio_count(self):
		acount = 0
		for f in self.frames:
			acount += f.acount()
		return acount

	def get_total_frames(self):
		return len(self.frames)

	def update_header(self):
		vcount = self.get_total_frames()
		acount = self.get_audio_count()
		mvsize = self.get_movi_size()
		self.header.update(vcount, acount, mvsize)

	def write_idx1(self, io):
		vcount = self.get_total_frames()
		acount = self.get_audio_count()

		idx1_size = 8 + 16*vcount + 16*acount

		io.write(b'idx1') # 4
		io.write(byt(idx1_size-8)) # 4

		offset = 4 # offset from movi_pos
		for f in self.frames:
			io.write(f.id)
			if f.is_iframe():
				io.write(b'\x10\x00\x00\x00')
			else:
				io.write(b'\x00\x00\x00\x00')
			io.write(byt(offset))
			io.write(f.size)
			offset += f.len_wo_audio()
			for a in f.audio_frames:
				io.write(a.id)
				io.write(b'\x10\x00\x00\x00')
				io.write(byt(offset))
				io.write(a.size)
				offset += len(a)

	def write_frames(self, io):
		for f in self.frames:
			f.write(io)

	def write(self, io):
		self.update_header()
		io.write(self.header.raw)
		self.write_frames(io)
		self.write_idx1(io)

	def save(self, file_name='', out_dir='', suffix=''):
		if not file_name:
			if not suffix:
				file_name = self.header.file_name.strip('.avi') + '_moshed.avi'
			else:
				file_name = self.header.file_name.strip('.avi') + suffix + '.avi'
		elif file_name[-4:] != '.avi':
			if file_name.count('.') > 0:
				raise ValueError('File name is improperly formatted. Must either have no extension or end in .avi')
			else:
				file_name += '.avi'
		if out_dir:
			# create method in tech to check validity of directory
			out_dir = out_dir + '/' if out_dir[-1] != '/' else out_dir
			file_pre = path.basename(file_name)
			file_name = out_dir + file_pre

		#print(file_name)
		save = open(file_name, 'wb')
		
		self.write(save)
		save.close()
		return file_name





	### =================== FRAME INFO METHODS ================= ###

	def get_iframe_indices(self):
		indices = []

		for i in range(len(self.frames)):
			f = self.frames[i]
			if f.is_keyframe():
				indices.append(i)

		return indices

	def get_keyframe_indices(self):
		return self.get_iframe_indices()

	def get_pframe_indices(self):
		indices = []

		for i in range(len(self.frames)):
			f = self.frames[i]
			if f.is_pframe():
				indices.append(i)

		return indices

	def get_deltaframe_indices(self):
		return self.get_pframe_indices()






	### ==================== MOSH METHODS ======================= ###

	def shuffle(self, repeat=False, num=10):
		indices = [*range(0, len(self))]
		random.shuffle(indices)
		if repeat:
			new = []
			for i in indices:
				for k in range(num):
					new.append(i)
			indices = new

		self.frames = [self.frames[i] for i in indices]

	def multiply(self, info, times=10, replace=False):
		if isinstance(info, int):
			temp_pre = self.frames[:info]
			if replace:
				temp_post = self.frames[info+times:]
			else:
				temp_post = self.frames[info:]
			multiply = []
			for i in range(times):
				multiply.append(self.frames[info])
			self.frames = temp_pre + multiply + temp_post
		else:
			raise IndexError('Dumbass')
			# implement info as a Frame (compare tags)

	def dupe(self, num, times=10, replace=False):
		for i in range(num):
			pframes = self.get_pframe_indices()
			index = random.choice(pframes)
			self.multiply(index, times, replace)

	def delete_keyframes(self, keep=1):
		new_frames = []
		count = 0

		for f in self.frames:
			if not f.is_iframe() or count < keep:
				if count < keep and f.is_iframe():
					count += 1
				new_frames.append(f)

		self.frames = new_frames


	def remap(self, target, replacement, chance=1000, frame_chance=100, start=0, end=100, keyframes=True):
		for f in self:
			rand = random.randint(0, 100)
			if rand <= frame_chance:
				if not keyframes and f.is_iframe():
					None
				else:
					f.has_remap = True
					f.remap_args = [target, replacement, chance, start, end]
					f.remap()
					f.has_remap = False

	def set_remaps(self, target, replacement, chance=1000, frame_chance=100, start=0, end=100, keyframes=True):
		for f in self:
			rand = random.randint(0, 100)
			if rand <= frame_chance:
				if not keyframes and f.is_iframe():
					None
				else:
					f.has_remap = True
					f.remap_args = [target, replacement, chance, start, end]

	def apply_remaps(self):
		for f in self:
			if f.has_remap:
				f.remap()
				f.has_remap = False




