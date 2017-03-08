import copy

class InvalidScoreException(Exception):
	pass

class GameOverException(Exception):
	pass


class Game:

	def __init__(self):
		self._frame = 1
		self._complete_frames = []
		self._curr_frame = None
		self._scores = []

	def roll(self, score):
		if len(self._complete_frames) == 10:
			raise GameOverException
		self._scores.append(score)
		self._frame, self._complete_frames, self._curr_frame = self._sort_frames(self._scores)
		return self._calculate_score(self._complete_frames, self._curr_frame)

	def _sort_frames(self, scores):
		curr = []
		complete = []
		for score in scores:
			curr.append(score)
			# this is basic logic
			# should be different from frame 10
			if self._is_frame_complete(len(complete) + 1, curr):
				complete.append(curr)
				curr = []
		number = len(complete) + 1
		return number, complete, curr

	@staticmethod
	def _is_frame_complete(number, frame):
		"""
		args:
			:number: (int) frame number
			:frame: (array) scores in this frame
		returns:
			boolean
		"""
		if number < 10:
			if sum(frame) == 10 or len(frame) == 2:
				return True
		else:
			# special case for 10th frame
			if len(frame) == 2 and sum(frame) < 10:
				return True
			if len(frame) == 3:
				return True
		return False

	@staticmethod
	def _calculate_score(completed_frames, curr_frame):
		frames = copy.copy(completed_frames)
		if curr_frame:
			frames.append(curr_frame)
		total_score = 0
		strikes = []
		spares = []
		rolls = []
		for frame in frames:
			total_score += sum(frame)
			if sum(frame) == 10:
				if frame[0] == 10:
					strikes.append(len(rolls))
				else:
					spares.append(len(rolls) + 1)
			rolls += frame
		# now to add the strike/spare bonuses:
		for strike in strikes:
			total_score += sum(rolls[strike+1:strike+3])
		for spare in spares:
			total_score += sum(rolls[spare+1:spare+2])
		return total_score

	def get_score(self):
		return self._calculate_score(self._complete_frames, self._curr_frame)