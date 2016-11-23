/**
 * Range function. return a list with value between the range defined;
 * @param {int} start - Initial value
 * @param {int} stop - Final value
 * @param {int} step - Step value
 * @returns {[int]}
 */
function range(start, stop, step){
  if (stop == undefined) {
    stop = start;
    start = 0;
  }

  var a=[start], b=start;

  if (step==undefined) {
    step = 1;
  }

  while(b<stop){
    b += step;
    a.push(b)
  }
  return a;
};