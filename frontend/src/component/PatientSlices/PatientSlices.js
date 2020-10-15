import React, { useState, useEffect } from 'react';
import './PatientSlices.css';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css'; 
import 'slick-carousel/slick/slick-theme.css';
import DicomImg from '../DicomImg/DicomImg';
import { Container, Row, Col } from 'react-bootstrap';

const PatientSlices = (props) => {
  const [scanDates, setScanDates] = useState([]);
  const [slices, setSlices] = useState({});

  useEffect(() => {
    if (props.slices) {
      setScanDates(Object.keys(props.slices).sort());
      for (const scanDate in props.slices) props.slices[scanDate].sort();
      setSlices(props.slices);
    }
  }, [props.patient, props.slices]);

  const settings = {
    dots: false,
    infinite: false,
    vertical: true,
    slidesToShow: 5,
    slidesToScroll: 3,
    swipeToSlide: true,
    verticalSwiping: true,
    draggable: true
  };

  const createSliders = (scanDate, i) => {
    return (
      <Col key={i}>
        {scanDate}: {props.answer[scanDate] ? props.answer[scanDate] : "未選択"}
        <Slider className="slides" {...settings}>
          {
            slices[scanDate].map((slice, j) => 
              <div className="slice" key={j} onClick={() => props.selectSlice(scanDate, slice)}><DicomImg
                imageId={`wadouri:http://localhost:5000/slice/${props.patient}/${scanDate}/${slice}`}
              /></div>)
          }
        </Slider>
      </Col>
    );
  }

  return (
    <div>
      <Container>
        <Row className="d-flex flex-nowrap">{scanDates.map(createSliders)}</Row>
      </Container>
    </div>
  );
};

export default PatientSlices;