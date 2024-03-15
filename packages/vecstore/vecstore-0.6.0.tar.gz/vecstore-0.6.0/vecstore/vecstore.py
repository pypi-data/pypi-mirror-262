import math
import numpy as np
from hnswlib import Index


class VecStore(Index):
    def __init__(self, fname, space='cosine', dim=512):  # 512 for sbert
        """
        creates empty store, serializable to file named "fname"
        containing vectors of size "dim"
        """
        super().__init__(space=space, dim=dim)
        self.fname = fname
        self.initialized = False

    def load(self):
        """ loads store content from file named "fname" """
        self.load_index(self.fname)

    def save(self):
        """ saves store content to file named "fname" """
        self.save_index(self.fname)

    def init(self, N=1024):
        """
        initializes store to default paprameters
        and max_elements=N
        """
        if self.initialized: return
        self.init_index(max_elements=N,
                        ef_construction=100,
                        M=64,
                        allow_replace_deleted=True
                        )
        self.set_ef(20)
        self.set_num_threads(8)
        self.initialized = True

    def add(self, xss):
        """
        adds numpy array of numpy vectors to store
        """
        self.init()
        if isinstance(xss,list): xss=np.array(xss)
        assert xss.shape[1] == self.dim
        N = xss.shape[0]
        N += self.element_count
        if N > self.max_elements:
            N = max(2 * self.max_elements, 2 ** math.ceil(math.log2(N)))
            self.resize_index(N)
        self.add_items(xss)

    def ids(self):
        """
        returns list of ids (natural numbers) for vecs in store
        """
        return sorted(self.get_ids_list())

    def vecs(self, as_list=False):
        """
        returns the list or numpy array of vectors in the store
        """
        return_type = 'list' if as_list else 'numpy'
        return self.get_items(self.ids(), return_type=return_type)

    def delete(self,i):
        """ deletes vector of id=i from the store """
        self.mark_deleted(i)

    def query(self, qss, k=3):
        """
         returns ids and knn similarity scores for k neares neightbor
         for each numpy vector (ok also in list form) in qss
        """
        assert isinstance(k, int)
        if isinstance(qss, list): qss = np.array(qss)
        distss,vect_idss = self.knn_query(qss, k, filter=None)
        return distss,vect_idss

    def query_one(self,qs,k=3):
        """
        returns knn for given k as pair of (scores,vector ids)
        """
        dists,vect_ids=self.query([qs],k=k)
        return dists[0],vect_ids[0]

def test_vecstore():
    """
    simple test of all operations excpe delete
    """
    vs = VecStore('temp.bin', dim=3)
    xss = [[11, 22, 33], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    yss = [[1, 2, 3], [30, 40, 50]]
    qs = [7, 8, 9]
    #xss = np.array(xss)
    yss = np.array(yss)
    #qss = np.array(qss)
    print(qs)

    vs.add(xss)
    vs.add(yss)

    print('IDS:\n',vs.ids())
    print('VECS:\n',vs.vecs())

    vs.save()
    vs_ = VecStore('temp.bin', dim=3)
    vs_.load()
    r = vs_.query_one(qs)
    print()
    print(r[0])
    print(r[1])


if __name__ == "__main__":
    test_vecstore()
