from tech import *
import random

class AudioFrame:

	def __init__(self, data):
		self.id = b'01wb'
		self.size = data[0:4]
		self.data = data[4:]

	def __len__(self):
		return 8 + len(self.data)

	def get_data(self):
		return self.data[:]

	def get_raw(self):
		return self.id + self.size + self.data

	def get_size(self):
		return num(self.size)

	def set_data(self, data):
		if not isinstance(data, bytes):
			raise TypeError('Data must be of type \'bytes\'.')
		self.data = data

		length = len(data)
		if length % 2 != 0:
			self.data += b'\x00'

		self.size = byt(length)

	def set_size(self, size):
		if not isinstance(data, int):
			raise TypeError('Size must be of type \'int\'.')
		self.size = byt(size)

	def write(self, io):
		io.write(self.id)
		io.write(self.size)
		io.write(self.data)
		return len(self)



class Frame:

	def __init__(self, data):
		self.id = b'00dc'
		self.size = data[0:4]
		self.flag = data[4:8]
		self.has_remap = False
		self.remap_args = []

		length = fix(num(self.size))

		self.data = data[8:length+4]
		self.audio_frames = []


		# allows to initialize audio frames directly as well
		# although we use set_audio_frames() for this purpose instead
		pos = length+4
		datal = len(data)
		while pos < datal:
			if data[pos:pos+4] != b'01wb':
				raise IndexError('data[length+4:length+8]: {}'.format(data[pos:pos+4]))
			
			curr_size = fix(num(data[pos+4:pos+8]))
			self.audio_frames.append(AudioFrame(data[pos+4:pos+8+curr_size]))
			pos += 8 + curr_size

	def __str__(self):
		ret = 'id: {}'.format(self.id)
		ret += '\nsize: {}'.format(num(self.size))
		ret += '\nflag: {}'.format(self.flag)
		ret += '\nacount: {}'.format(self.acount())
		return ret

	def set_audio_frames(self, array):
		for a in array:
			self.audio_frames.append(a)

	def __len__(self):
		length = 0
		for a in self.audio_frames:
			length += len(a)

		return 8 + len(self.flag) + len(self.data) + length

	def copy(self):
		frame_data = self.get_raw(False, False)
		new_frame = Frame(frame_data)
		new_frame.set_audio_frames(self.audio_frames)
		return new_frame

	def len_wo_audio(self):
		return 8 + len(self.flag) + len(self.data)

	def get_raw(self, id=True, audio=False):
		if id == False and audio == False:
			return self.size + self.flag + self.data
		elif id == True:
			return self.id + self.size + self.flag + self.data
		else:
			return self.id + self.size + self.flag + self.data + self.get_audio_data()

	def get_audio_data(self):
		data = b''
		for a in self.audio_frames:
			data += a.get_raw()
		return data

	def acount(self):
		return len(self.audio_frames)

	def has_audio(self):
		return self.acount() > 0

	def get_data(self):
		return self.data[:]

	def get_flag(self):
		return self.flag[:]

	def get_size(self):
		return num(self.size)

	def set_data(self, data):
		if not isinstance(data, bytes):
			raise TypeError('Data must be of type \'bytes\'.')
		self.data = data

		length = len(data)
		if length % 2 != 0:
			self.data += b'\x00'

		self.size = byt(length)

	def set_size(self, size):
		if not isinstance(data, int):
			raise TypeError('Size must be of type \'int\'.')
		self.size = byt(size)
		print('hi')

	def is_iframe(self):
		return self.flag == IFRAME

	def is_keyframe(self):
		return self.is_iframe()

	def is_pframe(self):
		return self.flag == PFRAME and not self.is_bframe()

	def is_deltaframe(self):
		return self.is_pframe()

	def is_bframe(self):
		return self.data[0:1].hex()[0] == '9'

	def write(self, io):
		io.write(self.id)
		io.write(self.size)
		io.write(self.flag)
		io.write(self.data)

		k = 0
		for a in self.audio_frames:
			a.write(io)

		return len(self)

	def remap(self):
		if not self.has_remap:
			raise ValueError('Trying to apply remap to frame that has no remap.')
		if len(self.remap_args) != 5:
			raise IndexError('Incorrect number of remap arguments. {}'.format())

		target = self.remap_args[0]
		replacement = self.remap_args[1]
		chance = self.remap_args[2]
		start = self.remap_args[3]
		end = self.remap_args[4]

		full = len(self.data) - 32
		if end <= start:
			raise IndexError('End percentage must be greater than start percentage.')

		start_index = int(round(full * start / 100))
		end_index = int(round(full * end / 100))
		first_part = self.data[0:32+start_index]
		last_part = self.data[32+end_index:]
		middle_part = bytearray(self.data[32+start_index:32+end_index])
		if chance == 1000:
			for i in range(len(middle_part)):
				if middle_part[i] == target:
					middle_part[i] = replacement
		else:
			indices = random.sample(range(len(middle_part)), round((chance/1000)*len(middle_part)))
			for i in indices:
				if middle_part[i] == target:
					middle_part[i] = replacement
		middle_part = bytes(middle_part)
		self.data = first_part + middle_part + last_part

		


class IndexFrame:
	def __init__(self, start, end, keyframe, bframe=False, empty=False):
		self.start = start
		self.size = end - start - 4
		self.keyframe = keyframe
		self.bframe = bframe
		self.empty = empty



	





