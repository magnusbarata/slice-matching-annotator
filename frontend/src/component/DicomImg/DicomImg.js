import React, { useState, useRef, useEffect } from 'react';
import * as cornerstone from 'cornerstone-core';
import dicomParser from 'dicom-parser';
import * as cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';
import './DicomImg.css';

cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
cornerstoneWADOImageLoader.external.dicomParser = dicomParser;

const DicomImg = (props) => {
  const [imageId, setImageId] = useState(props.imageId);
  const [viewport, setViewport] = useState(cornerstone.getDefaultViewport(null, undefined));
  const element = useRef(null);

  useEffect(() => {
    // Enable the DOM Element for use with Cornerstone
    cornerstone.enable(element.current);

    // Load image
    cornerstone.loadAndCacheImage(imageId).then(image => {
      cornerstone.displayImage(element.current, image);
    });

    return () => {
      cornerstone.disable(element.current);
    };
  }, []);

  return (
    <div>
      {
      <div className="dicomImg" ref={ element }>
        <canvas className="cornerstone-canvas" />
      </div>
      }
    </div>
  );
};

export default DicomImg;