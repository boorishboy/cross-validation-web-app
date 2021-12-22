
function getCVLabels(array) {
  var xlables = [];
  for (let i = 1; i - 1 < array.length; i++) {
    xlables.push(i.toString())
  }
  return xlables;
}

// function getRKFErrorArray(array, data) {
//   const errorArray = [];
//   for (let i = 0; i < array.length; i++) {
//     errorArray.push(data.results.cv_stddev)
//   }
//   return errorArray;
// }
//
// function getRKFMeanArray(array, data) {
//   const meanArray = [];
//   for (let i = 0; i < array.length; i++) {
//     meanArray.push(data.results.cv_mean)
//   }
//   return meanArray;
// }
//
// function getCVErrorArray(array, data) {
//   const errorArray = [];
//   for (let i = 0; i < array.length; i++) {
//     errorArray.push(data.results.cv_stddev)
//   }
//   return errorArray;
// }
//
// function getCVMeanArray(array, data) {
//   const meanArray = [];
//   for (let i = 0; i < array.length; i++) {
//     meanArray.push(data.results.cv_mean)
//   }
//   return meanArray;
// }

function getMeanArray(array, data){
  const meanArray = [];
  for (let i = 0; i < array.length; i++) {
    meanArray.push(data)
  }
  return meanArray;
}
function getMedianArray(array, data){
  const medianArray = [];
  for (let i = 0; i < array.length; i++) {
    medianArray.push(data)
  }
  return medianArray;
}

function getErrorArray(array, data) {
  const errorArray = [];
  for (let i = 0; i < array.length; i++) {
    errorArray.push(data)
  }
  return errorArray;
}


function plotRKF(dataRKF, data) {
  var trace1 = {
    x: getCVLabels(dataRKF),
    y: dataRKF,
    name: 'RKF Scores',
    error_y: {
      type: 'data',
      array: getErrorArray(dataRKF, data.results.cv_stddev),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getCVLabels(dataRKF),
    y: getMeanArray(dataRKF, data.results.cv_mean),
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
    x: getCVLabels(dataCV),
    y: dataCV,
    name: 'Cross Validation Scores',
    error_y: {
      type: 'data',
      array: getErrorArray(dataCV, data.results.cv_stddev),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getCVLabels(dataCV),
    y: getMeanArray(dataCV, data.results.cv_mean),
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

function plotOLS_first(y_data, percentage_error_vect_ols, data) {
  var trace1 = {
    x: y_data.slice(0, 75),
    y: percentage_error_vect_ols.slice(0, 75).map(function(x) {return x * 100.0}),
    name: 'percentage error BEEBS',
    mode: 'markers',
    type: 'scatter'
  };
  var trace2 = {
    x: y_data.slice(75),
    y: percentage_error_vect_ols.slice(75).map(function(x) {return x * 100.0}),
    name: 'percentage error IRIDA',
    mode: 'markers',
    type: 'scatter'
  };
  var trace3 = {
    x: y_data,
    y: getMeanArray(y_data, data.results.mean_percentage_error_ols * 100.0),
    name: 'Mean',
    type: 'line'
  };
  var trace4 = {
    x: y_data,
    y: getMedianArray(y_data, data.results.median_percentage_error_ols * 100.0),
    name: 'Median',
    type: 'line'
  };
  var data_ols = [trace1, trace2, trace3, trace4];
  var layout = {
    title: 'IDK tbh',
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      type: 'log',
      title: 'True values [J]',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    yaxis: {
      title: "Relative error [%]",
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
        filename: 'OLS-first',
        format: 'png'
    }
  };



   Plotly.newPlot('ols-first-plot', data_ols, layout, config);
}
