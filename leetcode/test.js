var MajorityChecker = function(arr) {
    this.arr = arr
    this.counter = []
};

/**
 * @param {number} left
 * @param {number} right
 * @param {number} threshold
 * @return {number}
 */
MajorityChecker.prototype.query = function(left, right, threshold) {
    this.counter = new Array(20001)
    if(right - left + 1 < threshold) {
        return -1
    }
    for(let i = left;i <= right;i++){
        let val = this.arr[i]
        this.counter[val] = this.counter[val] || 0
        if(++this.counter[val] >= threshold) {
            return val
        }
    }
    return -1
};