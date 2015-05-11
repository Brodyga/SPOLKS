from mpi4py import MPI
import numpy

N = 512

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

A = numpy.zeros(N * N)
B = numpy.zeros(N * N)
C = numpy.zeros(N * N)

if rank == 0:
	for i in range(N * N):
		A[i] = i + 1
		B[i] = i + 1

if (size > N):
	size = N + 1

comm.Bcast(B, root=0)
rows = int(N / (size - 1))
if rank == 0:
	start = MPI.Wtime()
	for i in range((size - 1)):
		if rows * (size - 1) == N:
			comm.Send(A[(i * N * rows) : (i + 1) * N * rows], dest=(i + 1), tag=0)
		else:
			if i == size - 2:
				comm.Send(A[(i * N * rows) :], dest=(i + 1), tag=0)
			else:
				comm.Send(A[(i * N * rows) : (i + 1) * N * rows], dest=(i + 1), tag=0)	

if rank != 0:
	if rows * (size - 1) != N and rank == size - 1:
		rows = rows + (N - (size - 1) * rows)
	
	comm.Recv(A[0 : rows * N], source=0, tag=0)
	for i in range(rows):
		for k in range(N):
			for j in range(N):
				C[i * N + j] += (A[i * N + k] * B[k * N + j])
	comm.Send(C[0 : rows * N], dest=0, tag=1)

if rank == 0:
	for i in range((size - 1)):
		comm.Recv(C[i * N * rows:], source=(i + 1), tag=1)

	end = MPI.Wtime()
	print (end - start)
	#for i in range(N):
	#	print C[(i * N) : (i + 1) * N]