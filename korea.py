import pandas as pd   # 판다스 사용 가능함
import matplotlib.pyplot as plt   # 드래프 그리기
import matplotlib.ticker as mtick   # 그래프 색 입히기

# 한글 깨짐
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 읽기
def load_data(file_path):
    return pd.read_csv(file_path, encoding='cp949')

# 데이터 전처리
def filter_general_households(df):
    df = df[df['성별'] == '계']
    drop_ages = ['15~64세', '65세이상']
    df = df[~df['연령별'].isin(drop_ages)]
    df = df[['성별', '연령별', '시점', '일반가구원']]
    return df

# 전처리 저장
def save_preprocessed_data(df, save_path):
    df.to_csv(save_path, index=False, encoding='cp949')
    print(f'전처리 데이터가 저장되었습니다: {save_path}')

# 연도별 통계
def total_stats(df):
    total_df = df[df['연령별'] == '합계']
    total_grouped = total_df.groupby('시점')['일반가구원'].sum()
    print('\n[연도별 전체 일반가구원 통계]')
    print(total_grouped.to_string())
    return total_grouped

# 연령별 통계
def age_stats(df):
    age_df = df[df['연령별'] != '합계']
    age_sum = age_df.groupby('연령별')['일반가구원'].sum()
    age_order = ['15세미만','15~19세','20~24세','25~29세','30~34세','35~39세',
                 '40~44세','45~49세','50~54세','55~59세','60~64세',
                 '65~69세','70~74세','75~79세','80~84세','85세이상']
    age_sum = age_sum.reindex(age_order)
    print('\n[연령별 일반가구원]')
    print(age_sum.to_string())
    return age_sum

def plot_age_trends(age_sum):
    plt.figure(figsize=(12,6))
    ax = plt.gca()

    # 구간별 배경색, index 순서에 맞춰 X축 좌표 지정
    age_index = list(range(len(age_sum)))
    ax.axvspan(age_index[0]-0.5, age_index[1]+0.5, color='skyblue', alpha=0.2)  # 15세미만~19세
    ax.axvspan(age_index[2]-0.5, age_index[5]+0.5, color='plum', alpha=0.2)      # 20~39세
    ax.axvspan(age_index[6]-0.5, age_index[11]+0.5, color='skyblue', alpha=0.2)  # 40~64세
    ax.axvspan(age_index[12]-0.5, age_index[15]+0.5, color='plum', alpha=0.2)    # 65세 이상

    # 꺾은선 그래프
    plt.plot(age_sum.index, age_sum.values, marker='o', linestyle='-', color='blue')
    plt.title('2015년 이후 연령별 일반가구원 총합')
    plt.xlabel('연령대')
    plt.ylabel('총 일반가구원 수')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)

    # Y축을 '천만' 단위로 표시
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f'{int(x/1e7)}천만'))

    plt.tight_layout()
    plt.show()


# 인구 변화 리포트
def analyze_trend(age_sum):
    print('\n[인구 변화 트렌드 리포트]')
    print('15세미만~19세   출생률 감소로 인한 급격한 감소')
    print('20~39세         경제 활동 인구 증가로 인한 점진적 증가')
    print('40~64세         안정적인 경제활동으로 인한 많은 인구')
    print('65세 이상       고령화 진행으로 인한 점진적 감소')

def main():
    file_path = 'data.csv'
    save_path = 'preprocessed_data.csv'

    df = load_data(file_path)   # csv 파일 읽기
    df = filter_general_households(df)   # 데이터 전처리
    save_preprocessed_data(df, save_path)   # 전처리 데이터 저장

    total_stats(df)   # 연도별 통계
    age_sum = age_stats(df)   # 연령별 통계

    analyze_trend(age_sum)   # 분석
    plot_age_trends(age_sum)   # 그래프

if __name__ == '__main__':
    main()
