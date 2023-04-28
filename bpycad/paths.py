import numpy as np

def twist_extrude_path(distance, num_segments, orientation_matrix, theta_step):
    inp_rot_mat = np.asarray(orientation_matrix)

    # create the pillar
    i_lin = np.asarray([np.linspace(0, distance, num_segments)])
    pts = i_lin.transpose() @ np.array([[0, 0, 1]])
    v0 = []
    v1 = []
    v2 = []
    for i in i_lin[0]:
        R = np.array([[np.cos(theta_step * i), -np.sin(theta_step * i), 0],
                      [np.sin(theta_step * i), np.cos(theta_step * i), 0],
                      [0, 0, 1]])
        v0.append(R[0, :])
        v1.append(R[1, :])
        v2.append(R[2, :])
    pts = pts @ inp_rot_mat
    v0 = np.asarray(v0) @ inp_rot_mat
    v1 = np.asarray(v1) @ inp_rot_mat
    v2 = np.asarray(v2) @ inp_rot_mat
    pt_mat_pairs = []
    for p in range(len(pts)):
        rot = np.asarray([v0[p],v1[p],v2[p]])
        pt_mat_pairs.append((pts[p], rot))

    return pt_mat_pairs
