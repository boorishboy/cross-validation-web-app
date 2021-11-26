
function getLabels(array) {
  var xlables = [];
  for (let i = 1; i - 1 < array.length; i++) {
    xlables.push(i.toString())
  }
  return xlables;
}

function getRKFErrorArray(array, data) {
  const errorArray = [];
  for (let i = 0; i < array.length; i++) {
    errorArray.push(data.results.cv_stddev)
  }
  return errorArray;
}

function getRKFMeanArray(array, data) {
  const meanArray = [];
  for (let i = 0; i < array.length; i++) {
    meanArray.push(data.results.cv_mean)
  }
  return meanArray;
}

function getCVErrorArray(array, data) {
  const errorArray = [];
  for (let i = 0; i < array.length; i++) {
    errorArray.push(data.results.cv_stddev)
  }
  return errorArray;
}

function getCVMeanArray(array, data) {
  const meanArray = [];
  for (let i = 0; i < array.length; i++) {
    meanArray.push(data.results.cv_mean)
  }
  return meanArray;
}

function plotRKF(dataRKF, data) {
  var trace1 = {
    x: getLabels(dataRKF),
    y: dataRKF,
    name: 'RKF Scores',
    error_y: {
      type: 'data',
      array: getRKFErrorArray(dataRKF, data),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getLabels(dataRKF),
    y: getRKFMeanArray(dataRKF, data),
    name: 'Mean',
    type: 'line'
  };
  var data_rkf = [trace1, trace2];
  var layout = {
    title: 'RepeatedKFold Scores',
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      'type': 'category',
      title: 'Number of Fold',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
    // shapes: [{
    //     type: 'line',
    //     x0: 1,
    //     y0: 0,
    //     x1: 1,
    //     y1: 2,
    //     line: {
    //       color: 'rgb(55, 128, 191)',
    //       width: 3
    //     }
    //   }
    // ]
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
        filename: 'CV_Scores',
        format: 'png'
    }
  };



   Plotly.newPlot('data-val-rkf-plot', data_rkf, layout, config);
}

function plotCV(dataCV, data) {
  var trace1 = {
    x: getLabels(dataCV),
    y: dataCV,
    name: 'Cross Validation Scores',
    error_y: {
      type: 'data',
      array: getCVErrorArray(dataCV, data),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getLabels(dataCV),
    y: getCVMeanArray(dataCV, data),
    name: 'Mean',
    type: 'line'
  };
  var data_cv = [trace1, trace2];
  var layout = {
    title: 'Cross Validation Scores',
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      'type': 'category',
      title: 'Number of Fold',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
    // shapes: [{
    //     type: 'line',
    //     x0: 1,
    //     y0: 0,
    //     x1: 1,
    //     y1: 2,
    //     line: {
    //       color: 'rgb(55, 128, 191)',
    //       width: 3
    //     }
    //   }
    // ]
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
        filename: 'CV_Scores',
        format: 'png'
    }
  };



   Plotly.newPlot('data-val-cv-plot', data_cv, layout, config);
}
