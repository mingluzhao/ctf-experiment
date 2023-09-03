import React from 'react';
import './SquareParent.css';
 
import redbase from './assets/redbase.png'
import bluebase from './assets/bluebase.png'
import redbaseflag from './assets/redbaseflag.png'
import bluebaseflag from './assets/bluebaseflag.png'

import obstacle from './assets/obstacle.png'
import border from './assets/border.png'


const SquareParent = ({ type, details, visible}) => {
  let content = null;

  switch (type) {
    case 'b':
      let baseImage
      if(details.hasflag === true){
        if(details.color === 'red'){
          baseImage = redbaseflag
        }
        else{
          baseImage = bluebaseflag
        }
      }
      else{
        if(details.color === 'red'){
          baseImage = redbase
        }
        else{
          baseImage = bluebase
        }
      }
      content = (
        <img
          src={baseImage} // Using the dynamically constructed image name
          alt={`${details.color} base`}
        />
      );
      break;
    case 'o':
      content = <img src={obstacle} alt="obstacle" />;
      break;
    case 'x':
      content = <img src={border} alt="border" />;
      break;
    case 'e':
      content = null;
      break;
    default:
      content = null;
  }

  let squareStyle = "square";

  if (type === 'e' && !visible) {
    squareStyle = "square-invisible";
  }

  return <div className={squareStyle}>{content}</div>;
};

export default SquareParent;