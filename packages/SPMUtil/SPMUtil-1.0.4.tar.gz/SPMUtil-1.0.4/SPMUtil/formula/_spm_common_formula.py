import numpy as np
from scipy import interpolate
import SPMUtil
from SPMUtil.structures.scan_data_format import PythonScanParam






def get_rotate_matrix(python_param: PythonScanParam):
    rot_z = python_param.ZRotation / 180 * np.pi
    pos_x = (python_param.Aux1MaxVoltage + python_param.Aux1MinVoltage) / 2
    pos_y = (python_param.Aux2MaxVoltage + python_param.Aux2MinVoltage) / 2
    return np.array([[np.cos(rot_z), -np.sin(rot_z), pos_x-pos_x*np.cos(rot_z)+pos_y*np.sin(rot_z)],
                    [np.sin(rot_z), np.cos(rot_z), pos_y-pos_x*np.sin(rot_z)-pos_y*np.cos(rot_z)],
                    [0,              0,          1]])



def rotate_scan_array(array_x, array_y, python_param: PythonScanParam):
    rot_matrix = get_rotate_matrix(python_param)
    if SPMUtil.use_cython:
        from SPMUtil.cython_files import cython_code
        res = cython_code.rotate_array(array_x, array_y, np.ndarray.flatten(rot_matrix))
        return res
    else:
        for i in range(0, len(array_x)):
            array_x[i], array_y[i], _ = np.matmul(rot_matrix, [array_x[i], array_y[i], 1])
        return array_x, array_y


def line_proline(map, xy_point_from, xy_point_to):
    length = int(np.hypot(xy_point_to[0] - xy_point_from[0], xy_point_to[1] - xy_point_from[1]))
    x, y = np.linspace(xy_point_from[0], xy_point_to[0], length), np.linspace(xy_point_from[1], xy_point_to[1], length)
    return map[y.astype(np.int64), x.astype(np.int64)]


def topo_map_correction(topo_map: np.ndarray, threshold=3):
    mean, std = np.mean(topo_map), np.std(topo_map)
    size = topo_map.shape
    threshold = threshold * std
    topo_map[abs(topo_map - mean) > threshold] = np.nan
    x, y = np.arange(0, size[1]), np.arange(0, size[0])
    array = np.ma.masked_invalid(topo_map)
    xx, yy = np.meshgrid(x, y)
    x1, y1 = xx[~array.mask], yy[~array.mask]

    map = interpolate.griddata((x1, y1), array[~array.mask].ravel(), (xx, yy), method="cubic")
    nans, x = np.isnan(map), lambda z: z.nonzero()[0]
    map[nans] = np.interp(x(nans), x(~nans), map[~nans])
    return map



def normalize01_2dmap(array):
    min, max = np.min(array), np.max(array)
    return (array - min) / (max - min)



def calc_ncc_dim3(template, image):
    if SPMUtil.use_cython:
        from SPMUtil.cython_files import cython_tm_code
        F = template.astype(np.float32)
        M = image.astype(np.float32)
        ncc = np.zeros(
            (M.shape[1] - F.shape[1]) * (M.shape[2] - F.shape[2])).astype(np.float32)
        cython_tm_code.c_calc_NCC_dim3(M.flatten().astype(np.float32), np.array(M.shape).astype(
            np.int32), F.flatten().astype(np.float32), np.array(F.shape).astype(np.int32), ncc)
        ncc = ncc.reshape([M.shape[1] - F.shape[1], M.shape[2] - F.shape[2]])
    else:
        c, h_f, w_f = template.shape
        tmp = np.zeros((c, image.shape[-2] - h_f, image.shape[-1] - w_f, h_f, w_f))
        for i in range(image.shape[-2] - h_f):
            for j in range(image.shape[-1] - w_f):
                M_tilde = image[:, i:i + h_f, j:j + w_f][None, None, :, :]
                tmp[:, i, j, :, :] = M_tilde / np.linalg.norm(M_tilde)
        ncc = np.sum(tmp * template.reshape(template.shape[-3], 1, 1, template.shape[-2], template.shape[-1]),
                     axis=(0, 3, 4))
    return ncc



def calc_SAD_dim3(template, image):
    if SPMUtil.use_cython:
        from SPMUtil.cython_files import cython_tm_code
        F = template.astype(np.float32)
        M = image.astype(np.float32)
        SAD = np.zeros(
            (M.shape[1] - F.shape[1]) * (M.shape[2] - F.shape[2])).astype(np.float32)
        cython_tm_code.c_calc_SAD_dim3(M.flatten().astype(np.float32), np.array(M.shape).astype(
            np.int32), F.flatten().astype(np.float32), np.array(F.shape).astype(np.int32), SAD)
        SAD = SAD.reshape([M.shape[1] - F.shape[1], M.shape[2] - F.shape[2]])
    else:
        c, h_f, w_f = template.shape
        tmp = np.zeros((c, image.shape[-2] - h_f, image.shape[-1] - w_f, h_f, w_f))
        for i in range(image.shape[-2] - h_f):
            for j in range(image.shape[-1] - w_f):
                M_tilde = image[:, i:i + h_f, j:j + w_f][None, None, :, :]
                tmp[:, i, j, :, :] = M_tilde
        SAD = np.sum(np.abs(tmp - template.reshape(c, 1, 1, h_f, w_f)), axis=(0, 3, 4))
    return np.max(SAD) - SAD



def calc_SSD_dim3(template, image, use_cython=False):
    if SPMUtil.use_cython:
        from SPMUtil.cython_files import cython_tm_code
        F = template.astype(np.float32)
        M = image.astype(np.float32)
        SSD = np.zeros(
            (M.shape[1] - F.shape[1]) * (M.shape[2] - F.shape[2])).astype(np.float32)
        cython_tm_code.c_calc_SSD_dim3(M.flatten().astype(np.float32), np.array(M.shape).astype(
            np.int32), F.flatten().astype(np.float32), np.array(F.shape).astype(np.int32), SSD)
        SSD = SSD.reshape([M.shape[1] - F.shape[1], M.shape[2] - F.shape[2]])
    else:
        c, h_f, w_f = template.shape
        tmp = np.zeros((c, image.shape[-2] - h_f, image.shape[-1] - w_f, h_f, w_f))
        for i in range(image.shape[-2] - h_f):
            for j in range(image.shape[-1] - w_f):
                M_tilde = image[:, i:i + h_f, j:j + w_f][None, None, :, :]
                tmp[:, i, j, :, :] = M_tilde
        SSD = np.sum(np.square(tmp - template.reshape(c, 1, 1, h_f, w_f)), axis=(0, 3, 4))
    return np.max(SSD) - SSD

