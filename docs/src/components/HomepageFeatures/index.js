import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'API 문서',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        검색과 관련된 API 정보를 제공합니다.
      </>
    ),
  },
  {
    title: '화면 및 기능 정의',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        각 화면 기능마다 호출하는 API와 발생 가능한 에러를 정의해 클라이언트 작업 시 참고할 수 있습니다.
      </>
    ),
  },
  {
    title: '검색 관련 서비스 안내',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        뉴스 검색과 관련된 여러 MSA 간의 구조,<br></br>데이터 플로우 등을 안내합니다.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
